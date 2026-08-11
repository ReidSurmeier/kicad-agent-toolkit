# Third-party components

- KiCAD-MCP-Server is included as a Git submodule under its MIT license. The
  fork and exact commit are recorded in `toolchain.lock.json`.
- KiCad is GPL licensed; KiBot is GPL licensed. Their pinned container contains
  additional components under their respective licenses.
- QMK Firmware is GPL-2.0-or-later and its container contains additional tools.
- Gerbv is GPL-2.0-or-later. PyGerber is MIT licensed.
- GitNexus 1.6.9 uses the PolyForm Noncommercial 1.0.0 license.
- Playwright Core 1.61.1 is Apache-2.0 licensed. The toolkit uses it to drive
  either a local Chromium-family browser or Browserbase over CDP.

This repository does not relicense those components. Consult each upstream
distribution for complete notices and source obligations.
