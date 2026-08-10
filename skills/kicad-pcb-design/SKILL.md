---
name: kicad-pcb-design
description: Design or modify KiCad schematics, PCB layouts, libraries, rules, routing, zones, and project outputs. Use for `.kicad_sch`, `.kicad_pcb`, `.kicad_pro`, footprint, placement, differential-pair, power/ground, USB, component-substitution, or fabrication-preparation work that requires source-backed engineering and authoritative KiCad verification.
---

# KiCad PCB design

Treat the schematic as the logical source of truth, the selected production
process as the rule source, and saved KiCad output as the verification surface.
A successful edit command proves execution only.

## Workflow

1. **Study.** Read [design-study.md](references/design-study.md). Create the
   requirements, exact-package pin maps, circuit evidence, manufacturing basis,
   critical-net matrix, and bring-up plan. Finish when every material decision
   has controlling evidence or a named blocker.
2. **Inventory.** Locate the root project, sheets, board, project libraries,
   rules, jobsets, generated outputs, and active backend state. Record the exact
   revision or source hashes.
3. **Inspect.** Read components, nets, outline, layers, rules, zones, locked
   objects, and critical-net geometry before editing. Read item properties;
   display color is not electrical evidence.
4. **Checkpoint.** Preserve a recoverable baseline with version control or an
   MCP project snapshot. Keep one consistent backend session.
5. **Mutate vertically.** Make one coherent circuit or layout change, save it,
   and read back the affected objects. Use dry-run modes for bulk operations.
6. **Prove the slice.** Apply [schematic-workflow.md](references/schematic-workflow.md)
   or [pcb-workflow.md](references/pcb-workflow.md). Resolve new findings before
   starting the next slice.
7. **Verify freshly.** Close the editing backend, hash the saved sources, open a
   clean KiCad process, refill zones, and run named `kicad-cli` ERC/DRC/export
   commands against those hashes. Capture version, command, status, output,
   timestamp, and report hashes.
8. **Inspect manufacturing truth.** Review copper, zones, mask, paste,
   silkscreen, outline, PTH/NPTH drills, BOM, placement, and 3D. Parse Gerbers
   and drills with a second implementation.
9. **Audit release.** Invoke `$kicad-design-review`. Report verified facts,
   engineering judgments, accepted risks, and bench-unverified claims separately.

## Non-negotiable engineering rules

- Trace each non-trivial circuit to the exact-device datasheet and an official
  application/reference circuit when available. Record every adaptation.
- Verify symbol pin numbers against the exact package and footprint pads.
- Derive widths, clearances, stackup, vias, mask, and assembly limits from the
  ordered process plus current, voltage, thermal, impedance, and safety needs.
- Encode enforceable critical constraints in KiCad. Name manual checks for
  criteria KiCad cannot enforce. DRC cannot check a rule that was never defined.
- Route USB and other differential interfaces as coupled systems with bounded
  breakouts/stubs, continuous reference, matched transitions, and reproducible
  coupled/uncoupled metrics. Total-length similarity alone is insufficient.
- Reconcile every intended plane pad from the netlist to the freshly filled
  zone as direct/thermal, trace-or-via-only, or missing; report islands and necks.
- Treat autorouter output as a draft. Inspect topology, return paths, widths,
  vias, clearances, plane continuity, and unrouted items before acceptance.
- Preserve authoritative failures. Retry a crash once from a clean process on
  the identical revision; leave the gate blocked until KiCad succeeds.
- Reserve “working” for executed physical tests. ERC, DRC, renders, simulation,
  and Gerber parsing do not prove enumeration, flashing, keys, EMC, or reliability.

## Tool use

Use the KiCad MCP server for structured inspection and controlled editing. Use
`kicad-cli` as independent ground truth. Discover MCP schemas instead of guessing
them. Read [mcp-operations.md](references/mcp-operations.md) when setup, backend,
save-divergence, or tool-discovery behavior is involved.
