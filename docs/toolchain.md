# Full KiCad agent pipeline

## Trust and version boundary

`toolchain.lock.json` is the machine-readable bill of materials. It pins the
KiCad/KiBot and QMK container digests, the MCP upstream and patched commits, and
the verified host-tool versions. The KiCad MCP is a Git submodule pointing to a
maintained fork. Its patch branch preserves the upstream release and fixes the
macOS interpreter precedence required for `pcbnew`; the advertised MCP server
version is also reconciled with the package release.

The derived release image pins its Debian package versions and installs the MCP
Python 3.13 environment from `requirements-mcp-python313.lock.txt`. Updating the
base digest or any package requires rebuilding and repeating the image
validation, MCP protocol smoke test, and container release fixture.

The recorded MCP evidence is 70 passing TypeScript tests, 1,710 passing Python
tests, 31 hardware/platform skips, and zero known npm vulnerabilities after the
lockfile refresh. Re-run those checks after any dependency or revision change.

## One CLI

```text
pcb-agent install     install skills, stage/build MCP, register it with Codex
pcb-agent doctor      report every host tool, registration, and credential state
pcb-agent validate    verify skill completeness and the pinned MCP revision
pcb-agent mcp test    negotiate MCP and discover its routing tools over stdio
pcb-agent release     build and independently verify a manufacturing package
```

All reports expose credential state only as `configured` or `not configured`.
No credential value is read into a report or copied into an installation.

## JLCPCB API boundary

The MCP recognizes `JLCPCB_APP_ID`, `JLCPCB_API_KEY`, and
`JLCPCB_API_SECRET`. Supply them to the Codex process through an OS keychain
wrapper or a short-lived inherited environment. Do not put them in `.env`,
`config.toml`, shell history, this repository, CI logs, or a fabrication ZIP.
API service access can remain unavailable while the corresponding JLCPCB app
services are under review. Rotate any key that has been pasted into chat or
another durable transcript before production use.

## Release evidence

The native gate runs KiCad ERC with all severities and violation exit codes,
then KiCad DRC with zone refill, schematic parity, all-track reporting, all
severities, and violation exit codes. It exports a netlist, BOM, positions,
schematic PDF, top/bottom renders, nine Gerber layers, and separate PTH/NPTH
drills. Gerbv parses the complete manufacturing set, and PyGerber independently
parses every Gerber layer. The exact upload ZIP is CRC-tested and hashed.

When not disabled explicitly, the same project is copied to a disposable
directory and processed by KiBot 1.9.1 and KiCad 10.0.4 in the pinned container.
Projects carrying one `firmware/qmk/*/keyboard.json` are also compiled using the
QMK commit and QMK CLI container pinned in the lockfile; the HEX is hashed into
the report.
The canonical source is hashed before and after; the release fails if it changes.
Existing output directories are preserved as timestamped backups.

`release-report.json`, logs, parser renders, `SHA256SUMS`, and the fabrication
ZIP are the evidence bundle. This proves checker cleanliness and manufacturing
file readability. It does not prove USB enumeration, firmware flashing, matrix
behavior, ESD/EMC performance, thermal margin, reliability, or assembly quality.
Those remain numeric physical bring-up gates.

## Sandboxing and portability

`docker compose run --rm pcb-agent` executes the release CLI inside a container
and mounts only the selected project directory. It therefore cannot inspect
unmounted personal files. For interactive Codex isolation, mount only the Git
workspace and a dedicated Codex home into a separately configured container;
never mount the host home directory or Docker socket.

The GitHub workflow checks out submodules, validates the toolkit, exercises the
safe installer seams, audits/builds the MCP, and runs its TypeScript suite.
Native KiCad and release integration remain local/container gates because the
host runner must provide the EDA dependencies.

## GitNexus

GitNexus is an optional code-graph index for maintaining the toolkit and MCP
fork. Version 1.6.9 is recorded in the lockfile. Its PolyForm Noncommercial
license is not equivalent to MIT; confirm that it fits the intended use before
installing or indexing. GitNexus analysis is supplemental and never substitutes
for tests, ERC, DRC, manufacturing parsing, or engineering review.
