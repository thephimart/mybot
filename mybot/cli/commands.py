"""CLI commands for mybot."""

import asyncio
import os
import select
import signal
import sys
from pathlib import Path
from typing import List

import typer
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.text import Text

from mybot import __logo__, __version__
from mybot.config.schema import Config

app = typer.Typer(
    name="mybot",
    help=f"{__logo__} mybot - Personal AI Assistant",
    no_args_is_help=True,
)

console = Console()
EXIT_COMMANDS = {"exit", "quit", "/exit", "/quit", ":q"}

# ---------------------------------------------------------------------------
# CLI input: prompt_toolkit for editing, paste, history, and display
# ---------------------------------------------------------------------------

_PROMPT_SESSION: PromptSession | None = None
_SAVED_TERM_ATTRS = None  # original termios settings, restored on exit


def _flush_pending_tty_input() -> None:
    """Drop unread keypresses typed while the model was generating output."""
    try:
        fd = sys.stdin.fileno()
        if not os.isatty(fd):
            return
    except Exception:
        return

    try:
        import termios

        termios.tcflush(fd, termios.TCIFLUSH)
        return
    except Exception:
        pass

    try:
        while True:
            ready, _, _ = select.select([fd], [], [], 0)
            if not ready:
                break
            if not os.read(fd, 4096):
                break
    except Exception:
        return


def _restore_terminal() -> None:
    """Restore terminal to its original state (echo, line buffering, etc.)."""
    if _SAVED_TERM_ATTRS is None:
        return
    try:
        import termios

        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, _SAVED_TERM_ATTRS)
    except Exception:
        pass


def _init_prompt_session() -> None:
    """Create the prompt_toolkit session with persistent file history."""
    global _PROMPT_SESSION, _SAVED_TERM_ATTRS

    # Save terminal state so we can restore it on exit
    try:
        import termios

        _SAVED_TERM_ATTRS = termios.tcgetattr(sys.stdin.fileno())
    except Exception:
        pass

    history_file = Path.home() / ".mybot" / "history" / "cli_history"
    history_file.parent.mkdir(parents=True, exist_ok=True)

    _PROMPT_SESSION = PromptSession(
        history=FileHistory(str(history_file)),
        enable_open_in_editor=False,
        multiline=False,  # Enter submits (single line mode)
    )


def _print_agent_response(response: str, render_markdown: bool) -> None:
    """Render assistant response with consistent terminal styling."""
    content = response or ""
    body = Markdown(content) if render_markdown else Text(content)
    console.print()
    console.print(f"[cyan]{__logo__} mybot[/cyan]")
    console.print(body)
    console.print()


def _is_exit_command(command: str) -> bool:
    """Return True when input should end interactive chat."""
    return command.lower() in EXIT_COMMANDS


async def _read_interactive_input_async() -> str:
    """Read user input using prompt_toolkit (handles paste, history, display).

    prompt_toolkit natively handles:
    - Multiline paste (bracketed paste mode)
    - History navigation (up/down arrows)
    - Clean display (no ghost characters or artifacts)
    """
    if _PROMPT_SESSION is None:
        raise RuntimeError("Call _init_prompt_session() first")
    try:
        with patch_stdout():
            return await _PROMPT_SESSION.prompt_async(
                HTML("<b fg='ansiblue'>You:</b> "),
            )
    except EOFError as exc:
        raise KeyboardInterrupt from exc


def version_callback(value: bool):
    if value:
        console.print(f"{__logo__} mybot v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(None, "--version", "-v", callback=version_callback, is_eager=True),
):
    """mybot - Personal AI Assistant."""
    pass


# ============================================================================
# Onboard / Setup
# ============================================================================


@app.command()
def onboard():
    """Initialize mybot configuration and workspace."""
    from mybot.config.loader import get_config_path, load_config, save_config
    from mybot.config.schema import Config
    from mybot.utils.helpers import get_workspace_path

    config_path = get_config_path()

    if config_path.exists():
        console.print(f"[yellow]Config already exists at {config_path}[/yellow]")
        console.print("  [bold]y[/bold] = overwrite with defaults (existing values will be lost)")
        console.print(
            "  [bold]N[/bold] = refresh config, keeping existing values and adding new fields"
        )
        if typer.confirm("Overwrite?"):
            config = Config()
            save_config(config)
            console.print(f"[green]✓[/green] Config reset to defaults at {config_path}")
        else:
            config = load_config()
            save_config(config)
            console.print(
                f"[green]✓[/green] Config refreshed at {config_path} (existing values preserved)"
            )
    else:
        save_config(Config())
        console.print(f"[green]✓[/green] Created config at {config_path}")

    # Create workspace
    workspace = get_workspace_path()

    if not workspace.exists():
        workspace.mkdir(parents=True, exist_ok=True)
        console.print(f"[green]✓[/green] Created workspace at {workspace}")

    # Create default bootstrap files
    _create_workspace_templates(workspace)

    console.print(f"\n{__logo__} mybot is ready!")
    console.print("\nNext steps:")
    console.print("  1. Add your API key to [cyan]~/.mybot/config.json[/cyan]")
    console.print("     Get one at: https://openrouter.ai/keys")
    console.print('  2. Chat: [cyan]mybot agent -m "Hello!"[/cyan]')


def _create_workspace_templates(workspace: Path):
    """Copy default workspace template files from package."""
    import shutil

    source_workspace = Path(__file__).parent.parent.parent / "workspace"

    if not source_workspace.exists():
        console.print("  [yellow]Warning: source templates not found[/yellow]")
        return

    for src_file in source_workspace.rglob("*"):
        if src_file.is_file():
            rel_path = src_file.relative_to(source_workspace)
            dest_file = workspace / rel_path

            if not dest_file.exists():
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dest_file)
                console.print(f"  [dim]Created {rel_path}[/dim]")


def _make_provider(config: Config):
    """Create LiteLLMProvider from config. Exits if no API key found."""
    from mybot.providers.litellm_provider import LiteLLMProvider
    from mybot.providers.openai_codex_provider import OpenAICodexProvider

    model = config.agents.defaults.model
    provider_name = config.get_provider_name(model)
    p = config.get_provider(model)

    # OpenAI Codex (OAuth): don't route via LiteLLM; use the dedicated implementation.
    if provider_name == "openai_codex" or model.startswith("openai-codex/"):
        return OpenAICodexProvider(default_model=model)

    if not model.startswith("bedrock/") and not (p and p.api_key):
        console.print("[red]Error: No API key configured.[/red]")
        console.print("Set one in ~/.mybot/config.json under providers section")
        raise typer.Exit(1)

    return LiteLLMProvider(
        api_key=p.api_key if p else None,
        api_base=config.get_api_base(model),
        default_model=model,
        extra_headers=p.extra_headers if p else None,
        provider_name=provider_name,
    )


# ============================================================================
# Gateway / Server
# ============================================================================


@app.command()
def gateway(
    port: int = typer.Option(18790, "--port", "-p", help="Gateway port"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """Start the mybot gateway."""
    from mybot.agent.loop import AgentLoop
    from mybot.bus.queue import MessageBus
    from mybot.channels.manager import ChannelManager
    from mybot.config.loader import get_data_dir, load_config
    from mybot.cron.service import CronService
    from mybot.cron.types import CronJob
    from mybot.heartbeat.service import HeartbeatService
    from mybot.session.manager import SessionManager

    if verbose:
        import logging

        logging.basicConfig(level=logging.DEBUG)

    console.print(f"{__logo__} Starting mybot gateway on port {port}...")

    config = load_config()
    bus = MessageBus()
    provider = _make_provider(config)
    session_manager = SessionManager(config.workspace_path)

    # Create cron service first (callback set after agent creation)
    cron_store_path = get_data_dir() / "cron" / "jobs.json"
    cron = CronService(cron_store_path)

    # Create agent with cron service
    agent = AgentLoop(
        bus=bus,
        provider=provider,
        workspace=config.workspace_path,
        model=config.agents.defaults.model,
        temperature=config.agents.defaults.temperature,
        max_tokens=config.agents.defaults.max_tokens,
        max_iterations=config.agents.defaults.max_tool_iterations,
        memory_window=config.agents.defaults.memory_window,
        exec_config=config.tools.exec,
        web_config=config.tools.web,
        cron_service=cron,
        restrict_to_workspace=config.tools.restrict_to_workspace,
        session_manager=session_manager,
        mcp_servers=config.tools.mcp_servers,
        subagent_config=config.agents.subagents,
        config=config,
    )

    # Set cron callback (needs agent)
    async def on_cron_job(job: CronJob) -> str | None:
        """Execute a cron job through the agent."""
        response = await agent.process_direct(
            job.payload.message,
            session_key=f"cron:{job.id}",
            channel=job.payload.channel or "cli",
            chat_id=job.payload.to or "direct",
        )
        if job.payload.deliver and job.payload.to:
            from mybot.bus.events import OutboundMessage

            await bus.publish_outbound(
                OutboundMessage(
                    channel=job.payload.channel or "cli",
                    chat_id=job.payload.to,
                    content=response or "",
                )
            )
        return response

    cron.on_job = on_cron_job

    # Create heartbeat service
    async def on_heartbeat(prompt: str) -> str:
        """Execute heartbeat through the agent."""
        return await agent.process_direct(prompt, session_key="heartbeat")

    heartbeat = HeartbeatService(
        workspace=config.workspace_path,
        on_heartbeat=on_heartbeat,
        interval_s=30 * 60,  # 30 minutes
        enabled=True,
    )

    # Create channel manager
    channels = ChannelManager(config, bus)

    if channels.enabled_channels:
        console.print(f"[green]✓[/green] Channels enabled: {', '.join(channels.enabled_channels)}")
    else:
        console.print("[yellow]Warning: No channels enabled[/yellow]")

    cron_status = cron.status()
    if cron_status["jobs"] > 0:
        console.print(f"[green]✓[/green] Cron: {cron_status['jobs']} scheduled jobs")

    console.print("[green]✓[/green] Heartbeat: every 30m")

    async def run():
        try:
            await cron.start()
            await heartbeat.start()
            await asyncio.gather(
                agent.run(),
                channels.start_all(),
            )
        except KeyboardInterrupt:
            console.print("\nShutting down...")
        finally:
            await agent.close_mcp()
            heartbeat.stop()
            cron.stop()
            agent.stop()
            await channels.stop_all()

    asyncio.run(run())


# ============================================================================
# Agent Commands
# ============================================================================


@app.command()
def agent(
    message: str = typer.Option(None, "--message", "-m", help="Message to send to the agent"),
    session_id: str = typer.Option("cli:direct", "--session", "-s", help="Session ID"),
    image: List[str] = typer.Option(
        None, "--image", "-i", help="Image file path or URL (can be repeated)"
    ),
    audio: List[str] = typer.Option(
        None, "--audio", "-a", help="Audio file path to transcribe (can be repeated)"
    ),
    markdown: bool = typer.Option(
        True, "--markdown/--no-markdown", help="Render assistant output as Markdown"
    ),
    logs: bool = typer.Option(
        False, "--logs/--no-logs", help="Show mybot runtime logs during chat"
    ),
):
    """Interact with the agent directly. Run without arguments for interactive mode."""
    from loguru import logger

    from mybot.agent.loop import AgentLoop
    from mybot.bus.queue import MessageBus
    from mybot.config.loader import load_config

    config = load_config()

    bus = MessageBus()
    provider = _make_provider(config)

    if logs:
        logger.enable("mybot")
    else:
        logger.disable("mybot")

    agent_loop = AgentLoop(
        bus=bus,
        provider=provider,
        workspace=config.workspace_path,
        model=config.agents.defaults.model,
        temperature=config.agents.defaults.temperature,
        max_tokens=config.agents.defaults.max_tokens,
        max_iterations=config.agents.defaults.max_tool_iterations,
        memory_window=config.agents.defaults.memory_window,
        exec_config=config.tools.exec,
        restrict_to_workspace=config.tools.restrict_to_workspace,
        mcp_servers=config.tools.mcp_servers,
        subagent_config=config.agents.subagents,
        config=config,
    )

    # Download URL images to local files (same workflow as Telegram)
    async def download_url_images(images: list[str]) -> list[str]:
        import hashlib
        import mimetypes

        import httpx

        local_paths = []
        media_dir = config.workspace_path / "media"
        media_dir.mkdir(parents=True, exist_ok=True)

        for img in images:
            if img.startswith(("http://", "https://")):
                try:
                    console.print(f"[dim]Downloading image...[/dim]")
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        resp = await client.get(img, follow_redirects=True)
                        resp.raise_for_status()

                        # Get extension from content-type or URL
                        content_type = resp.headers.get("content-type", "")
                        ext = mimetypes.guess_extension(content_type) or ".jpg"
                        if ext == ".jpe":
                            ext = ".jpg"

                        # Save to media dir with hash-based filename
                        url_hash = hashlib.md5(img.encode()).hexdigest()[:16]
                        file_path = media_dir / f"{url_hash}{ext}"
                        file_path.write_bytes(resp.content)

                        local_paths.append(str(file_path))
                        console.print(f"[dim]Saved to {file_path}[/dim]")
                except Exception as e:
                    console.print(f"[yellow]Warning: Failed to download image: {e}[/yellow]")
            else:
                # Already a local path
                local_paths.append(img)

        return local_paths

    media = None
    if image:
        media = asyncio.run(download_url_images(image))

    # Transcribe audio files
    audio_transcription = ""
    if audio:
        from mybot.providers.transcription import get_transcriber

        # Download URL audio to local files (same workflow as images)
        async def download_url_audio(audios: list[str]) -> list[str]:
            import hashlib
            import mimetypes

            import httpx

            local_paths = []
            media_dir = config.workspace_path / "media"
            media_dir.mkdir(parents=True, exist_ok=True)

            for audio_url in audios:
                if audio_url.startswith(("http://", "https://")):
                    try:
                        console.print(f"[dim]Downloading audio...[/dim]")
                        async with httpx.AsyncClient(timeout=60.0) as client:
                            resp = await client.get(audio_url, follow_redirects=True)
                            resp.raise_for_status()

                            content_type = resp.headers.get("content-type", "")
                            ext = mimetypes.guess_extension(content_type) or ".wav"
                            if ext == ".octet-stream":
                                ext = ".wav"

                            url_hash = hashlib.md5(audio_url.encode()).hexdigest()[:16]
                            file_path = media_dir / f"{url_hash}{ext}"
                            file_path.write_bytes(resp.content)

                            local_paths.append(str(file_path))
                            console.print(f"[dim]Saved to {file_path}[/dim]")
                    except Exception as e:
                        console.print(f"[yellow]Warning: Failed to download audio: {e}[/yellow]")
                else:
                    local_paths.append(audio_url)

            return local_paths

        local_audio = asyncio.run(download_url_audio(audio))

        groq_key = config.providers.groq.api_key if config.providers.groq else None
        transcriber = get_transcriber(
            use_local=config.transcriber.use_local,
            whisper_model=config.transcriber.whisper_model,
            device=config.transcriber.device,
            groq_api_key=groq_key,
        )
        console.print("[dim]Transcribing audio...[/dim]")

        async def transcribe_all():
            transcriptions = []
            for audio_file in local_audio:
                text = await transcriber.transcribe(audio_file)
                if text:
                    transcriptions.append(text)
            return " | ".join(transcriptions) if transcriptions else ""

        audio_transcription = asyncio.run(transcribe_all())
        if audio_transcription:
            console.print(f"[dim]Transcription: {audio_transcription[:100]}...[/dim]")

    # Show spinner when logs are off (no output to miss); skip when logs are on
    def _thinking_ctx():
        if logs:
            from contextlib import nullcontext

            return nullcontext()
        # Animated spinner is safe to use with prompt_toolkit input handling
        return console.status("[dim]mybot is thinking...[/dim]", spinner="dots")

    if message:
        # Append audio transcription to message (same workflow as Telegram)
        if audio_transcription:
            message = f"{message}\n\n[Audio transcription: {audio_transcription}]"

        # Single message mode
        async def run_once():
            with _thinking_ctx():
                response = await agent_loop.process_direct(message, session_id, media=media)
            _print_agent_response(response, render_markdown=markdown)
            await agent_loop.close_mcp()

        asyncio.run(run_once())
    else:
        # Interactive mode
        _init_prompt_session()
        console.print(
            f"{__logo__} Interactive mode (type [bold]exit[/bold] or [bold]Ctrl+C[/bold] to quit)\n"
        )

        def _exit_on_sigint(signum, frame):
            _restore_terminal()
            console.print("\nGoodbye!")
            os._exit(0)

        signal.signal(signal.SIGINT, _exit_on_sigint)

        async def run_interactive():
            try:
                while True:
                    try:
                        _flush_pending_tty_input()
                        user_input = await _read_interactive_input_async()
                        command = user_input.strip()
                        if not command:
                            continue

                        if _is_exit_command(command):
                            _restore_terminal()
                            console.print("\nGoodbye!")
                            break

                        with _thinking_ctx():
                            response = await agent_loop.process_direct(user_input, session_id)
                        _print_agent_response(response, render_markdown=markdown)
                    except KeyboardInterrupt:
                        _restore_terminal()
                        console.print("\nGoodbye!")
                        break
                    except EOFError:
                        _restore_terminal()
                        console.print("\nGoodbye!")
                        break
            finally:
                await agent_loop.close_mcp()

        asyncio.run(run_interactive())


# ============================================================================
# Channel Commands
# ============================================================================


channels_app = typer.Typer(help="Manage channels")
app.add_typer(channels_app, name="channels")


@channels_app.command("status")
def channels_status():
    """Show channel status."""
    from mybot.config.loader import load_config

    config = load_config()

    table = Table(title="Channel Status")
    table.add_column("Channel", style="cyan")
    table.add_column("Enabled", style="green")
    table.add_column("Configuration", style="yellow")

    # Telegram
    tg = config.channels.telegram
    tg_config = f"token: {tg.token[:10]}..." if tg.token else "[dim]not configured[/dim]"
    table.add_row("Telegram", "✓" if tg.enabled else "✗", tg_config)

    console.print(table)


# ============================================================================
# Cron Commands
# ============================================================================

cron_app = typer.Typer(help="Manage scheduled tasks")
app.add_typer(cron_app, name="cron")


@cron_app.command("list")
def cron_list(
    all: bool = typer.Option(False, "--all", "-a", help="Include disabled jobs"),
):
    """List scheduled jobs."""
    from mybot.config.loader import get_data_dir
    from mybot.cron.service import CronService

    store_path = get_data_dir() / "cron" / "jobs.json"
    service = CronService(store_path)

    jobs = service.list_jobs(include_disabled=all)

    if not jobs:
        console.print("No scheduled jobs.")
        return

    table = Table(title="Scheduled Jobs")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Schedule")
    table.add_column("Status")
    table.add_column("Next Run")

    import time

    for job in jobs:
        # Format schedule
        if job.schedule.kind == "every":
            sched = f"every {(job.schedule.every_ms or 0) // 1000}s"
        elif job.schedule.kind == "cron":
            sched = job.schedule.expr or ""
        else:
            sched = "one-time"

        # Format next run
        next_run = ""
        if job.state.next_run_at_ms:
            next_time = time.strftime(
                "%Y-%m-%d %H:%M", time.localtime(job.state.next_run_at_ms / 1000)
            )
            next_run = next_time

        status = "[green]enabled[/green]" if job.enabled else "[dim]disabled[/dim]"

        table.add_row(job.id, job.name, sched, status, next_run)

    console.print(table)


@cron_app.command("add")
def cron_add(
    name: str = typer.Option(..., "--name", "-n", help="Job name"),
    message: str = typer.Option(..., "--message", "-m", help="Message for agent"),
    every: int = typer.Option(None, "--every", "-e", help="Run every N seconds"),
    cron_expr: str = typer.Option(None, "--cron", "-c", help="Cron expression (e.g. '0 9 * * *')"),
    at: str = typer.Option(None, "--at", help="Run once at time (ISO format)"),
    deliver: bool = typer.Option(False, "--deliver", "-d", help="Deliver response to channel"),
    to: str = typer.Option(None, "--to", help="Recipient for delivery"),
    channel: str = typer.Option(
        None, "--channel", help="Channel for delivery (e.g. 'telegram', 'email')"
    ),
):
    """Add a scheduled job."""
    from mybot.config.loader import get_data_dir
    from mybot.cron.service import CronService
    from mybot.cron.types import CronSchedule

    # Determine schedule type
    if every:
        schedule = CronSchedule(kind="every", every_ms=every * 1000)
    elif cron_expr:
        schedule = CronSchedule(kind="cron", expr=cron_expr)
    elif at:
        import datetime

        dt = datetime.datetime.fromisoformat(at)
        schedule = CronSchedule(kind="at", at_ms=int(dt.timestamp() * 1000))
    else:
        console.print("[red]Error: Must specify --every, --cron, or --at[/red]")
        raise typer.Exit(1)

    store_path = get_data_dir() / "cron" / "jobs.json"
    service = CronService(store_path)

    job = service.add_job(
        name=name,
        schedule=schedule,
        message=message,
        deliver=deliver,
        to=to,
        channel=channel,
    )

    console.print(f"[green]✓[/green] Added job '{job.name}' ({job.id})")


@cron_app.command("remove")
def cron_remove(
    job_id: str = typer.Argument(..., help="Job ID to remove"),
):
    """Remove a scheduled job."""
    from mybot.config.loader import get_data_dir
    from mybot.cron.service import CronService

    store_path = get_data_dir() / "cron" / "jobs.json"
    service = CronService(store_path)

    if service.remove_job(job_id):
        console.print(f"[green]✓[/green] Removed job {job_id}")
    else:
        console.print(f"[red]Job {job_id} not found[/red]")


@cron_app.command("enable")
def cron_enable(
    job_id: str = typer.Argument(..., help="Job ID"),
    disable: bool = typer.Option(False, "--disable", help="Disable instead of enable"),
):
    """Enable or disable a job."""
    from mybot.config.loader import get_data_dir
    from mybot.cron.service import CronService

    store_path = get_data_dir() / "cron" / "jobs.json"
    service = CronService(store_path)

    job = service.enable_job(job_id, enabled=not disable)
    if job:
        status = "disabled" if disable else "enabled"
        console.print(f"[green]✓[/green] Job '{job.name}' {status}")
    else:
        console.print(f"[red]Job {job_id} not found[/red]")


@cron_app.command("run")
def cron_run(
    job_id: str = typer.Argument(..., help="Job ID to run"),
    force: bool = typer.Option(False, "--force", "-f", help="Run even if disabled"),
):
    """Manually run a job."""
    from mybot.config.loader import get_data_dir
    from mybot.cron.service import CronService

    store_path = get_data_dir() / "cron" / "jobs.json"
    service = CronService(store_path)

    async def run():
        return await service.run_job(job_id, force=force)

    if asyncio.run(run()):
        console.print("[green]✓[/green] Job executed")
    else:
        console.print(f"[red]Failed to run job {job_id}[/red]")


# ============================================================================
# Status Commands
# ============================================================================


@app.command()
def status():
    """Show mybot status."""
    # SECURITY: Load raw JSON only — no pydantic, no secrets in memory
    # NOTE: status MUST NOT call load_config() or instantiate ProviderConfig
    import json
    from pathlib import Path

    from mybot.config.loader import get_config_path

    config_path = get_config_path()
    with open(config_path) as f:
        cfg = json.load(f)

    workspace = cfg.get("agents", {}).get("defaults", {}).get("workspace", "<unset>")
    workspace_ok = workspace != "<unset>" and Path(workspace).expanduser().exists()

    console.print(f"{__logo__} mybot Status\n")
    console.print(
        f"Config: {config_path} {'[green]✓[/green]' if config_path.exists() else '[red]✗[/red]'}"
    )
    console.print(
        f"Workspace: {workspace} {'[green]✓[/green]' if workspace_ok else '[red]✗[/red]'}"
    )

    if config_path.exists():
        from mybot.providers.registry import PROVIDERS

        defaults = cfg.get("agents", {}).get("defaults", {})
        model = defaults.get("model", "<unset>")
        provider = defaults.get("provider", "<unset>")
        console.print(f"Model: {model}")
        if provider != "<unset>":
            console.print(f"Provider: {provider}")

        transcriber = cfg.get("transcriber", {})
        trans_type = "local" if transcriber.get("useLocal") else "groq"
        whisper_model = transcriber.get("whisperModel", "base")
        device = transcriber.get("device", "cpu")
        console.print(f"Transcriber: {trans_type} ({whisper_model}, {device})")

        providers = cfg.get("providers", {})
        for spec in PROVIDERS:
            parts = spec.name.split("_")
            key = parts[0] + "".join(p.title() for p in parts[1:])  # nvidia_nim → nvidiaNim
            p = providers.get(key, {})
            has_key = bool(p.get("apiKey"))
            has_base = bool(p.get("apiBase"))
            if has_key or has_base:
                if has_base:
                    console.print(f"{spec.label}: [green]✓ {p.get('apiBase')}[/green]")
                else:
                    console.print(f"{spec.label}: [green]✓[/green]")


# ============================================================================
# OAuth Login
# ============================================================================

provider_app = typer.Typer(help="Manage providers")
app.add_typer(provider_app, name="provider")


@provider_app.command("login")
def provider_login(
    provider: str = typer.Argument(
        ..., help="OAuth provider to authenticate with (e.g., 'openai-codex')"
    ),
):
    """Authenticate with an OAuth provider."""
    console.print(f"{__logo__} OAuth Login - {provider}\n")

    if provider == "openai-codex":
        try:
            from oauth_cli_kit import get_token, login_oauth_interactive

            token = None
            try:
                token = get_token()
            except Exception:
                token = None
            if not (token and token.access):
                console.print(
                    "[cyan]No valid token found. Starting interactive OAuth login...[/cyan]"
                )
                console.print("A browser window may open for you to authenticate.\n")
                token = login_oauth_interactive(
                    print_fn=lambda s: console.print(s),
                    prompt_fn=lambda s: typer.prompt(s),
                )
            if not (token and token.access):
                console.print("[red]✗ Authentication failed[/red]")
                raise typer.Exit(1)
            console.print("[green]✓ Successfully authenticated with OpenAI Codex![/green]")
            console.print(f"[dim]Account ID: {token.account_id}[/dim]")
        except ImportError:
            console.print("[red]oauth_cli_kit not installed. Run: pip install oauth-cli-kit[/red]")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Authentication error: {e}[/red]")
            raise typer.Exit(1)
    else:
        console.print(f"[red]Unknown OAuth provider: {provider}[/red]")
        console.print("[yellow]Supported providers: openai-codex[/yellow]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
