# Schematic workflow

1. Complete the design-study pack and inspect existing sheets, symbols, nets,
   and project libraries.
2. Verify each external part's exact package, pinout, units, hidden power pins,
   exposed pad, startup/strap states, ratings, and required support circuits.
3. Build each functional block from its evidence record. Record every departure
   from the official reference and validate the new operating conditions.
4. Annotate deterministically; assign footprints, exact MPNs, sourcing fields,
   ratings, tolerances, and population state.
5. Connect by verified pin identity. Use named/hierarchical nets where they make
   topology explicit. Add no-connect markers only after datasheet review.
6. Validate from the root schematic. Generate an authoritative netlist, run ERC,
   export every page, and inspect the render.

## Connectivity proof

Require all of these:

- Root ERC has no untriaged findings.
- Netlist maps every critical net to the expected `{reference.pin}` set.
- Exact-package pin maps independently match symbol pins and footprint pads.
- Render shows intended junctions, labels, crossings, hierarchy, and unused pins.
- Values, ratings, startup behavior, fault paths, and firmware dependencies have
  manual evidence; ERC does not establish them.

Use before/after net-to-pin diffs for cosmetic or bulk changes intended to
preserve topology. Treat a mutation success count as an execution receipt only.

## Common hazards

- Place wire anchors on KiCad's connection grid and lint off-grid endpoints.
- Place every required unit of a multi-unit symbol, including power units.
- Use one valid driver per power net: a real power output or an intentional
  `PWR_FLAG` for a passive/connector-fed rail.
- Reopen and revalidate after repairing flat vendor symbols or deleting wired
  components; search for orphaned wires and pin-coincident labels.

Finish only after the saved root source, netlist, ERC report, and inspected render
agree. Circuit function remains a separate engineering and bench claim.
