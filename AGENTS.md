# Agent operating contract

Use `skills/kicad-pcb-design` for design changes, `skills/kicad-design-review`
for independent release audits, and `skills/kicad-toolchain-setup` for machine
setup or diagnostics.

Treat exact-part sources and authoritative KiCad output as controlling evidence.
Keep generated reports tied to a source hash. A crashed or unavailable ERC/DRC
leaves its gate blocked. Separate design-check evidence from physical function.

Keep this repository portable: use repository-relative paths, respect
`CODEX_HOME`, and store credentials only in environment variables or an OS
keychain. Never commit downloaded copyrighted textbooks, tokens, API secrets,
machine-specific MCP configuration, or personal absolute paths.

Run the public validation interfaces after changes:

```bash
./scripts/validate.py --repo .
./scripts/install.sh --dry-run
```
