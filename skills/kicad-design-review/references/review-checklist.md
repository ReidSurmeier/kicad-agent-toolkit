# Technical review checklist

## Requirements and circuit

- Function, rail limits/current, environment, safety, interfaces/edges, clocks,
  EMC/ESD, programming, test, enclosure, stackup, and manufacturing are explicit.
- Power tree, reset/boot, sequencing, protection, grounding, isolation, and fault
  behavior match those requirements.
- Every non-trivial block has exact-part sources, an official reference when
  available, recorded adaptations, calculations/ratings, firmware dependencies,
  and a resolved confidence state.
- Every critical net has source-backed constraints, KiCad rules, and named manual
  checks for unenforceable criteria.

## Schematic and libraries

- Root reaches all sheets; references, values, MPNs, footprints, and population
  flags are complete.
- Connector numbering/mating view, every power pin/exposed pad, decoupling, bias,
  unused pins, protection, level compatibility, termination, and test access are
  intentional.
- Netlist critical pin sets match requirements and exact-package datasheets.
- Symbol pin, footprint pad, land pattern, drill/plating, paste/mask, courtyard,
  polarity, pin 1, body, and 3D assumptions match the exact package variant.
- Root ERC has no untriaged finding; a second pin-map pass is retained.

## PCB and outputs

- Outline/cutouts, mounting, keepouts, connector access, enclosure fit, stackup,
  and rules match the selected production options.
- Placement controls loops, returns, clocks, switchers, protection, antennas,
  sensors, high current, rework, probing, and assembly access.
- Routing is complete and widths/vias/impedance/clearance/creepage/layer changes/
  stubs/edge clearances are justified.
- Differential metrics define endpoints, coupled/uncoupled threshold, pad/via/
  breakout treatment, raw data, and visual reconciliation.
- Fresh zones reconcile every expected plane pad and report islands, necks,
  split-reference crossings, return stitching, and thermal paths.
- Gerber/drill layer set, outline, PTH/NPTH, mask, paste, legend, BOM, CPL side,
  rotation, origin, and assembly-process assignments are independently checked.
- When assembly is in scope, the exact uploaded BOM/CPL and manufacturer preview
  agree on every reference, package, side, rotation, polarity, DNP, origin, and
  process. Without that preview, fabrication may be ready but assembly is not.

## Evidence

Retain source hashes, evidence pack, authoritative netlist/ERC/DRC, renders,
critical metrics, footprint comparisons, manufacturing parses, unresolved risks,
and bring-up plan. Each fresh-process report includes command, tool/version,
source hash, status, output, timestamp, and report hash.
