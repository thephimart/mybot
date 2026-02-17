# Security Policy

mybot is a **local-first, fork-first bot core**.

There is no hosted service, no central authority, and no guaranteed security response.
**You are responsible for how your bot is deployed and secured.**

This document describes:
- the security assumptions mybot makes
- the risks you must understand
- the practices you are expected to follow

---

## Reporting vulnerabilities

If you discover a security issue **in this repository**:

- Do **not** open a public issue describing the vulnerability
- If this is your fork, fix it in your fork
- If you believe the issue exists in upstream mybot code, report it privately to the repository owner

There is **no SLA** and no guarantee of response time.

mybot is not a product — it is a codebase.

---

## Threat model (important)

mybot assumes:

- You run it on a machine you control
- You trust the user account running the process
- You understand what tools you enable
- You review code before deploying it

If you expose mybot to untrusted users or networks, **you must harden it yourself**.

---

## API keys & secrets

**Never commit secrets to version control.**

Recommended practices:

- Store secrets in a local config file with restricted permissions
- Or inject them via environment variables
- Rotate keys regularly
- Use separate keys for development and production

Example (Linux/macOS):

```bash
chmod 600 ~/.mybot/config.json
```

If your fork stores secrets differently, document it clearly for anyone who deploys it.

---

## Tool execution (critical)

mybot can execute tools, including shell commands.

You are expected to:

* Review every enabled tool
* Understand exactly what commands can be run
* Run mybot as a **non-root user**
* Use OS-level permissions to sandbox access

**Never run mybot as root.**

Reducing tools is a valid security strategy.
Deleting code is encouraged.

---

## File system access

Built-in file tools include basic path protections, but **they are not a sandbox**.

Best practices:

* Run under a dedicated user account
* Restrict filesystem permissions at the OS level
* Limit access to only required directories
* Audit file operations during development

If you need strong isolation, use containers, VMs, or mandatory access controls.

---

## Network access

mybot makes outbound network requests to:

* LLM providers
* Optional external services you configure

Recommendations:

* Use HTTPS endpoints only
* Apply firewall rules if running on a server
* Monitor outbound traffic
* Set spending limits on API providers

There is no inbound network access unless you add it

---

## Dependencies

Keep dependencies updated.

If you fork mybot, **you own dependency security**.

Suggested tooling:

```bash
pip install pip-audit
pip-audit
```

Remove dependencies you don’t need.
Fewer dependencies = smaller attack surface.

---

## Channels & access control

If your fork exposes messaging channels:

* Always restrict who can interact with the bot
* Do not leave public endpoints open by default
* Log access attempts where possible

If you don’t need remote interaction, **remove channels entirely**.

---

## Logs & data

Be aware:

* Logs may contain prompts, responses, or file paths
* Local memory may contain sensitive data
* LLM providers see your prompts

Protect logs and data directories with filesystem permissions.

---

## Known limitations

mybot intentionally does **not** provide:

* Rate limiting
* User authentication frameworks
* Encrypted secret storage
* Automatic session expiry
* Centralized audit trails

If you need these features, add them in your fork.

---

## Incident response (your responsibility)

If you suspect a compromise:

1. Revoke exposed API keys immediately
2. Stop the bot
3. Review logs and recent changes
4. Rotate credentials
5. Patch or remove the affected code
6. Re-deploy in a clean environment

---

## Philosophy

Security in mybot comes from:

* minimal code
* explicit behavior
* local control
* informed operators

If you don’t understand what your bot can do, it is not secure.

---

## License

MIT License.
Security responsibility transfers with the code.
