# KiCad Agent Toolkit

Portable Codex skills, engineering references, and deterministic checks for
evidence-driven KiCad design and fabrication review.

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
- `scripts/`: portable installer, validator, and release checker.
- `tests/`: public-interface tests for those scripts.

## Install on another machine

Clone the repository, then run:

```bash
./scripts/install.sh
./scripts/validate.py --repo .
./scripts/release-check.sh /path/to/project.kicad_pro
```

The installer respects `CODEX_HOME`; when it is unset, it uses `~/.codex`.
Machine credentials belong in environment variables or an OS keychain. This
repository contains no JLCPCB keys, GitHub tokens, or personal absolute paths.

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
