# Platform installation branches

Use official installation instructions and pin or record the installed versions.
Package names and capabilities change; verify current upstream documentation
before executing an install.

## macOS

- Install KiCad and Docker Desktop from their official packages or Homebrew
  casks: `brew install --cask kicad docker`.
- Install the independent parser and runtimes: `brew install gerbv node python`.
- Install the version-pinned Python parser in an isolated environment. First
  resolve `codex_home="${CODEX_HOME:-$HOME/.codex}"`, then run
  `python3 -m venv "$codex_home/tools/pygerber-venv"` and
  `"$codex_home/tools/pygerber-venv/bin/pip" install pygerber==2.4.3`.
  Prefer the repository installer when it already provides a working
  `pygerber`.
- Install GitNexus 1.6.9 only when its PolyForm Noncommercial license fits the
  intended use: `npm install -g gitnexus@1.6.9`.
- Use Docker for a clean Linux KiCad/KiBot verification process when the project
  requires cross-environment evidence.

## Linux

- Prefer the KiCad project repository or distribution packages documented by
  KiCad for the selected distribution.
- Install KiBot using its documented package/container method.
- Install Gerbv, Python virtual environments, Node, and GitHub CLI from their
  official distribution paths.

## KiCad MCP server

Do not independently clone an unpinned release. Initialize the repository
submodule and run `./pcb-agent install`; the lockfile binds the upstream release,
the maintained patch commit, zero-vulnerability npm audit result, and test
counts. `./pcb-agent mcp test` must negotiate MCP initialization and discover the
three routing tools. On macOS, `KICAD_PYTHON` must name KiCad's bundled Python,
while `PYTHONPATH` names the MCP virtual environment's packages.

## Acceptance

The toolchain is ready only when a disposable fixture can run: project parse,
root ERC, PCB DRC, Gerber/PTH/NPTH export, independent parsing, KiBot outputs,
and MCP discovery/readback. GitNexus index/query is required only when its
license fits the intended use. Otherwise run `pcb-agent install --skip-gitnexus`,
record the license-based waiver, and use ordinary `rg`, tests, and code review;
GitNexus is supplemental and never a PCB release gate.
