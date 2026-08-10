---
name: kicad-design-review
description: Independently audit KiCad schematics, PCB layouts, libraries, rules, and manufacturing packages. Use for ERC/DRC signoff, footprint and pin-map verification, USB or power/ground review, Gerber/drill/BOM/CPL inspection, DFM/assembly review, release readiness, or any claim that a board is fabrication-ready or verified.
---

# KiCad design review

Review the saved artifact independently from its design narrative. Prefer fresh
generated evidence and file readback over notes or prior success messages.

## Review loop

1. **Scope.** Identify function, electrical limits, interfaces, environment,
   stackup, enclosure, assembly process, target manufacturer, test strategy, and
   the exact reviewed revision. Missing controlling inputs are review gaps.
2. **Baseline.** Hash the source files, inventory sheets/libraries/board/rules,
   close loaded editing sessions, and render the schematic and PCB.
3. **Electrical.** Apply [review-checklist.md](references/review-checklist.md).
   Trace each non-trivial block to exact-part evidence, verify critical pin maps
   and topology, generate an authoritative netlist, and run whole-project ERC.
4. **Physical.** Check exact footprints, package variants, outline/mechanics,
   production rules, placement, routing, return paths, zones, thermals, test
   access, assembly access, silkscreen, and mask/paste behavior. Refill zones and
   run DRC in a clean process against the recorded source hash.
5. **Manufacturing.** Regenerate outputs from the reviewed source. Inspect every
   Gerber and drill layer with an independent parser. Reconcile BOM population,
   CPL side/rotation/origin, PTH-versus-SMT process, and the assembler preview
   when assembly is in scope. Without a preview, report fabrication and assembly
   readiness separately.
6. **Findings.** Classify each as blocker, major, minor, or informational. Name
   evidence, location/reference/net/layer, consequence, smallest safe correction,
   and the recheck required to close it.
7. **Verdict.** Apply [release-gates.md](references/release-gates.md) and return
   `ready`, `ready with accepted risks`, or `not ready`. Do not silently fix a
   review-only request.

## Evidence discipline

- Capture tool/version, exact command, source hash, exit status, stdout/stderr,
  timestamp, and report hash for authoritative checks.
- Treat exclusions and suppressions as engineering decisions, not clean results.
- Define differential metrics by endpoints, coupling threshold, pad/via and
  breakout treatment, units, and raw output; corroborate them visually.
- Reconcile the expected netlist pad set for every plane against filled-zone
  attachment state and report islands, bottlenecks, and trace-only attachments.
- A crashed authoritative checker gets one clean identical-revision retry. A
  supplemental script can diagnose but cannot substitute for KiCad ERC/DRC.
- Distinguish electrical correctness, rule cleanliness, manufacturability,
  assemblability, and functional adequacy. Passing one does not imply the others.
- Keep the physical bring-up gate open until numerical tests have actually run.
