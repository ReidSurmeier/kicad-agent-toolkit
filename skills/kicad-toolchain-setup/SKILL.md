---
name: kicad-toolchain-setup
description: Install, migrate, or diagnose the portable KiCad agent toolchain for Codex. Use when setting up another macOS or Linux machine, installing the bundled KiCad skills, configuring the KiCad MCP server, KiBot, Gerbv, PyGerber, GitNexus, or checking why CLI/MCP/ERC/DRC/release tooling is unavailable or crashing.
---

# KiCad toolchain setup

Build a reproducible CLI-first environment. Keep desktop automation optional;
the release path must remain operable from a terminal and clean process.

## Setup sequence

1. Inspect OS/architecture, package manager, Codex home, KiCad version, Python,
   Node, Docker, GitHub CLI, and existing MCP configuration. Preserve working
   installations and report version conflicts.
2. Run `./pcb-agent install --dry-run --json`, inspect its `prerequisites` and
   `destinations`, read [platforms.md](references/platforms.md), and resolve any
   missing host prerequisites. Use `./pcb-agent doctor --json` for the detailed
   installed-version and registration state.
3. Run `./pcb-agent install`. It atomically installs the three skill bundles,
   stages the pinned audited MCP fork under `CODEX_HOME/tools`, builds its Node
   and Python environments, and registers its stdio command with Codex. Existing
   toolkit installations are moved into timestamped recoverable backups.
4. Do not persist JLCPCB credentials on the user's behalf. Have the user inject
   them into the Codex process through inherited environment variables or a
   user-owned OS keychain wrapper. Use the exact names `JLCPCB_APP_ID`,
   `JLCPCB_API_KEY`, and `JLCPCB_API_SECRET`. Never place their values in Git,
   Codex skill files, shell history, examples, or generated reports.
5. Run `./pcb-agent doctor --json` and retain its machine-readable report. Confirm
   `kicad-cli`, ERC/DRC, Gerber/drill export, independent parsing, KiBot, MCP tool
   discovery, and GitNexus indexing on a disposable fixture project.
6. Run `./pcb-agent validate`, `./pcb-agent mcp test`, and
   `./pcb-agent release examples/tenkey-macropad/source/TenKeyMacroPad.kicad_pro`.
   Restart Codex and confirm the three installed skills are discoverable.

The bundled release command is a JLCPCB-style two-layer profile and expects the
project's `.kibot.yaml`. A missing configuration blocks the default release.
For a different manufacturer, add a manufacturer-specific, test-covered output
profile before claiming release readiness; do not merely rename the ZIP.

## Portability rules

- Resolve paths relative to the repository or `CODEX_HOME`; avoid personal
  absolute paths and assumptions about Homebrew prefixes.
- Pin or record tool versions. Treat “latest” as an explicit upgrade decision.
- Keep proprietary or licensed EDA packages optional. SPICE can supplement a
  circuit review but cannot validate PCB routing, USB enumeration, footprints,
  assembly, or manufacturing outputs.
- Keep the KiCad GUI useful for human inspection while making all release gates
  reproducible from CLI commands.
- On a CLI crash, preserve the command/output and source hash, retry once from a
  clean process, and leave the gate blocked if the authoritative tool still fails.

## Secrets boundary

Use placeholders such as `JLCPCB_API_KEY` and `JLCPCB_API_SECRET` in examples.
The setup process may verify that variables exist, but it must never print their
values or serialize them into reports. If the variables are absent, report the
API as `not configured` and continue with offline sourcing/release checks; do not
invent a persistence mechanism.
