"""Restart tool for gateway restart requests."""

import asyncio
from typing import Any

from mybot.agent.tools.base import Tool


class RestartTool(Tool):
    """Tool to request gateway restart via systemd."""

    def __init__(self, service_name: str = "mybot"):
        self._service_name = service_name

    @property
    def name(self) -> str:
        return "restart"

    @property
    def description(self) -> str:
        return f"Request gateway restart via systemd --user for {self._service_name}."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {},
            "required": [],
        }

    async def execute(self, **kwargs: Any) -> str:
        try:
            process = await asyncio.create_subprocess_exec(
                "systemctl",
                "--user",
                "restart",
                self._service_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=15)

            if process.returncode == 0:
                return f"Restart requested for {self._service_name}. Gateway will restart."
            else:
                err = stderr.decode() if stderr else "unknown error"
                return f"Failed to restart: {err}"
        except asyncio.TimeoutError:
            return "Restart command timed out"
        except FileNotFoundError:
            return "systemctl not found. Requires systemd user service."
        except Exception as e:
            return f"Error: {str(e)}"
