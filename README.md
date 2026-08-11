# KiCad Agent Toolkit

Portable Codex skills, an audited KiCad MCP fork, engineering references, and
deterministic checks for evidence-driven KiCad design and fabrication review.

This repository turns one successful ten-key macropad redesign into a reusable
workflow. It does **not** claim that ERC, DRC, rendering, or Gerber parsing proves
that a circuit works. A design becomes functionally verified only after the
documented physical bring-up tests pass.

## Included skills

- `kicad-pcb-design`: study, capture, place, route, and verify KiCad projects.
- `kicad-design-review`: independently audit source and manufacturing packages.
- `kicad-toolchain-setup`: install and diagnose the portable CLI/MCP toolchain.

## Repository map

- `skills/`: installable Codex skills and their progressive-disclosure references.
- `docs/curriculum/`: source hierarchy and design-study curriculum.
- `docs/sources/`: claim-to-source comparison and redistribution policy.
- `docs/case-studies/`: lessons extracted from the ten-key USB-C board.
- `examples/tenkey-macropad/`: sanitized design evidence and selected source files.
- `pcb-agent`: one public CLI for install, diagnosis, validation, MCP testing,
  release generation, and supplemental external DFM analysis.
- `vendor/KiCAD-MCP-Server/`: pinned submodule for the audited MCP fork.
- `toolchain.lock.json`: exact revisions, container digests, versions, licenses,
  audit counts, and upstream test evidence.
- `Dockerfile` and `compose.yaml`: sandboxed, reproducible release environment.
- `tests/`: public-interface tests for the pipeline.

## Install on another machine

Clone with submodules, inspect the plan, then install:

```bash
git clone --recurse-submodules https://github.com/ReidSurmeier/kicad-agent-toolkit.git
cd kicad-agent-toolkit
./pcb-agent install --dry-run
./pcb-agent install
./pcb-agent doctor
./pcb-agent validate
./pcb-agent mcp test
```

The installer respects `CODEX_HOME`; when it is unset, it uses `~/.codex`.
Machine credentials belong in environment variables or an OS keychain. This
repository contains no JLCPCB keys, GitHub tokens, or personal absolute paths.

## Release a project

```bash
./pcb-agent release /path/to/Board.kicad_pro
```

This bundled release profile is intentionally JLCPCB-style and requires a
project `.kibot.yaml`. It is not a universal manufacturer profile. Add and test
a supplier-specific profile for another fabricator; do not just rename the ZIP.

The default gate runs whole-project ERC and DRC, exports fabrication and
assembly files, renders both PCB sides, parses every Gerber with PyGerber,
parses the complete Gerber/drill set with Gerbv, runs the project `.kibot.yaml`
in the digest-pinned container, verifies the ZIP CRC, hashes the evidence, and
proves that the source files did not change. If `firmware/qmk/*/keyboard.json`
is present, it also compiles the default keymap against the pinned QMK checkout
and AVR toolchain. The upload artifact is
`outputs/release/<project>/fabrication/<project>-JLCPCB.zip`.

## Run supplemental external DFM

Generate the fabrication archive first, then explicitly authorize its upload to
NextPCB HQDFM Online:

```bash
./pcb-agent dfm outputs/release/Board/fabrication/Board-JLCPCB.zip \
  --allow-upload --browser-backend local
```

For unattended runs, inject `BROWSERBASE_API_KEY` from a user-owned secret
wrapper and select `--browser-backend browserbase`. The key is inherited by the
runner and is never written to the report. The command uploads through the
provider's normal public web interface, downloads and parses the PDF, records
source and report hashes, and returns nonzero if the report has findings or
cannot be interpreted. Browserbase's temporary report download is deleted after
local retrieval.

This does not bypass JLCPCB API approval. JLCDFM's public page uses an ordinary
JLCPCB account session; the toolkit does not replay private endpoints or evade
that login. HQDFM is the supported no-login alternative and remains an
independent supplemental check, not JLCPCB process approval or proof of physical
function. Review the fabrication data and the provider's current data terms
before using `--allow-upload`.

To run the entire release in a container, place the project directory in
`PCB_PROJECT_DIR` and its project filename in `PCB_PROJECT_FILE`:

```bash
PCB_PROJECT_DIR=/path/to/project PCB_PROJECT_FILE=Board.kicad_pro docker compose run --rm pcb-agent
```

See [the full pipeline](docs/toolchain.md) for installation branches, MCP,
Browserbase and JLCPCB credential boundaries, release/DFM evidence, CI,
GitNexus, and limitations.

## Evidence policy

Use the exact component datasheet, errata, interface specification, official
reference circuit, selected fabricator capabilities, and authoritative KiCad
output for the design being reviewed. Textbooks and community boards are
learning and comparison material, not substitutes for controlling sources.

See [the curriculum](docs/curriculum/design-study.md), [source comparison](docs/sources/comparison.md),
and [TenKey case study](docs/case-studies/tenkey-macropad.md).

## License

Code and original documentation are MIT licensed. Third-party documents and
designs remain under their own licenses and are represented by citations or
metadata unless redistribution is explicitly permitted.
