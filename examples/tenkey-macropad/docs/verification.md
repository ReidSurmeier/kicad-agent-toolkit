# Verification record

Date: 2026-08-09  
KiCad CLI / pcbnew: 10.0.5

## Passed release gates

| Check | Result | Evidence |
|---|---|---|
| Native schematic ERC, all severities | 0 violations | `outputs/release/validation/macos/erc-all.json` |
| Native PCB DRC | 0 violations, 0 unconnected, 0 schematic-parity issues | `outputs/release/validation/macos/drc-all.json` |
| Clean-container jobset | 6/6 jobs pass | `outputs/release/logs/native-jobset.log` |
| KiBot | ERC/DRC and all manufacturing outputs pass; 0 unique warnings | `outputs/release/logs/kibot.log` |
| Matrix contract | 10 switches, 10 diodes, no mapping errors | `outputs/release/validation/structural-audit.json` |
| Assembly-side contract | Front population is exactly SW1–SW10; all 34 other electrical references are on B.Cu | `outputs/release/validation/structural-audit.json` |
| Named-net connectivity | 0 open edges | `outputs/release/validation/structural-audit.json` |
| Supplemental exact-shape clearance | 0 copper/copper or copper/pad collisions | `outputs/release/validation/structural-audit.json` |
| Ground system | Filled F.Cu/B.Cu GND planes and ground audit pass | `outputs/release/validation/ground-connectivity-audit.json` |
| Power width | No +5 V or VBUS segment below 0.381 mm | `outputs/release/validation/structural-audit.json` |
| USB routing | Every USB segment is 0.20 mm; connector path skew remains below the encoded 4 mm limit | `outputs/release/validation/structural-audit.json` |
| Footprints | 48/48 pad geometries match pinned library geometry | `outputs/release/validation/footprint-geometry-audit.json` |
| Firmware contract | 35/35 checks pass; pinned HEX hash matches | `outputs/release/validation/supplemental/firmware-contract-check.json` |
| BOM/CPL | 44 schematic components covered; 30 SMT placements, all bottom side; J1 excluded as THT | `outputs/release/validation/augmentation-check.json`, `outputs/release/assembly/TenKeyMacroPad-SMT-CPL.csv` |
| Fabrication archive | 9 Gerbers + PTH/NPTH drills; ZIP CRC/member verification passes | `outputs/release/validation/release-verification.json` |
| Independent parser 1 | gerbv parses/renders every Gerber and both drill files | `outputs/release/inspection/gerbv/` |
| Independent parser 2 | PyGerber parses/renders every Gerber; front paste is empty | `outputs/release/inspection/pygerber/` |
| Release integrity | Core release and augmented release checks pass | `outputs/release/validation/release-verification.json`, `augmentation-check.json` |

Gerbv is an independent RS-274X/Excellon viewer and parser: <https://gerbv.github.io/>. PyGerber is an independent Gerber X2/X3 parser and renderer based on Ucamco's format specification: <https://github.com/Argmaster/pygerber>.

## Release verdict and mandatory limits

The CAD, manufacturing-package, firmware-build, and artifact-integrity checks pass. This is a **design-checks-passed / supplier-DFM release candidate**, not proof of a physically working board.

Two release constraints remain:

1. J1 is a through-hole part and needs a confirmed wave/selective/manual assembly step; it is intentionally absent from the 30-row SMT CPL.
2. No board has been assembled or bench-tested. Before a working/production claim, execute `docs/bring-up-plan.md`: current-limited power-up, rail/clock/reset checks, USB-C enumeration in both orientations, DFU/ISP recovery, all-key/ghosting tests, and soak testing.

The prototype firmware identity `FEED:0010` is not an owned commercial USB VID/PID and must be replaced before commercial distribution.
