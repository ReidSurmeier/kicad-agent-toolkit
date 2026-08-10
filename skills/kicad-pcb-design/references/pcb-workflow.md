# PCB workflow

## Transfer and constraints

Synchronize from the verified schematic and review every addition, removal, net
change, and footprint replacement. Define the outline, cutouts, mounting,
keepouts, ordered stackup, netclasses, custom rules, copper-to-edge, track/via,
differential, creepage/clearance, mask, and assembly constraints before routing.

Source each number from the manufacturer, interface/device data, calculations,
and safety needs. A remembered width or clearance is not a universal rule.

## Placement

Place mechanical features, connectors, protection, switches, antennas, sensors,
and enclosure-constrained parts first. Then place major ICs and their local
decoupling, clock, regulator, termination, and programming circuits. Preserve
signal-flow order, short current loops, continuous return channels, probe/rework
access, polarity visibility, cable clearance, courtyard, and assembly access.

## Routing and copper

- Route clocks, USB/differential interfaces, sensitive analog paths, switching
  loops, and high-current paths before ordinary signals.
- Keep each differential main run coupled with consistent geometry, bounded and
  symmetric breakouts, minimal stubs, matched transitions, continuous reference,
  and nearby return stitching at reference changes.
- Size power paths and vias from current, copper, allowable temperature rise,
  voltage drop, transient demand, and reliability. Report the narrowest segment.
- Refill zones after topology changes. Reconcile expected plane pads, islands,
  necks, thermal/direct connections, and trace/via-only attachments.
- Inspect autorouter results as candidates; reject accidental detours, broken
  returns, unnecessary vias, rule-minimum crowding, and incomplete topology.

## Verification and outputs

1. Save, close the editing backend, and record source hashes.
2. In a fresh process refill zones, run schematic parity and full DRC, and capture
   tool/version, command, status, output, timestamp, and report hashes.
3. Report critical-net metrics with their complete measurement definitions and
   reconcile them against highlighted front/back/filled-zone views.
4. Inspect mask, paste, silkscreen, outline/cutouts, PTH/NPTH drills, and 3D.
5. Generate Gerber/drill, BOM, position, schematic, assembly, and STEP outputs
   required by the selected manufacturer.
6. Parse manufacturing files independently and inspect each layer plus composites.
7. Invoke `$kicad-design-review` against the released source and outputs.

One clean process may retry an authoritative crash against the identical source
hash. If it still fails, preserve the evidence and leave the release gate blocked.
