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
2. Read [platforms.md](references/platforms.md), select the matching branch, and
   install KiCad, KiBot, Gerbv, PyGerber, GitNexus, and the KiCad MCP server from
   their pinned upstream sources.
3. Run the repository installer. It copies only the three skill bundles into
   `${CODEX_HOME:-~/.codex}/skills` and never copies credentials.
4. Register the MCP server using environment variables or an OS keychain for any
   secret. Never place API keys in Git, skill files, shell history, or examples.
5. Run `scripts/doctor.sh` and retain its machine-readable report. Confirm
   `kicad-cli`, ERC/DRC, Gerber/drill export, independent parsing, KiBot, MCP tool
   discovery, and GitNexus indexing on a disposable fixture project.
6. Restart Codex, verify that all three skills are discoverable, and run the
   repository validation suite.

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

Use placeholders such as `JLCPCB_ACCESS_KEY` and `JLCPCB_SECRET_KEY` in examples.
The setup process may verify that variables exist, but it must never print their
values or serialize them into reports.
