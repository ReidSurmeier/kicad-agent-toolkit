# Platform installation branches

Use official installation instructions and pin or record the installed versions.
Package names and capabilities change; verify current upstream documentation
before executing an install.

## macOS

- Install KiCad from the official KiCad package or current Homebrew cask.
- Install Python in an isolated environment for KiBot and PyGerber.
- Install Gerbv and GitHub CLI with Homebrew when available.
- Use Docker for a clean Linux KiCad/KiBot verification process when the project
  requires cross-environment evidence.

## Linux

- Prefer the KiCad project repository or distribution packages documented by
  KiCad for the selected distribution.
- Install KiBot using its documented package/container method.
- Install Gerbv, Python virtual environments, Node, and GitHub CLI from their
  official distribution paths.

## KiCad MCP server

Clone the pinned upstream revision into a user-owned tools directory, build its
Node entrypoint, create its Python environment as documented, run upstream tests,
and register its stdio command with Codex. Store the install directory in MCP
configuration rather than embedding it in the skills.

## Acceptance

The toolchain is ready only when a disposable fixture can run: project parse,
root ERC, PCB DRC, Gerber/PTH/NPTH export, independent parsing, KiBot outputs,
MCP discovery/readback, and GitNexus index/query. Record versions and failures.
