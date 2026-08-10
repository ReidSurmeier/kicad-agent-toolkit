# TenKey macropad case study

This case study records what the agent learned while converting an unreliable
four-key routing exercise into a ten-key, native-USB board. It is evidence about
a workflow, not a universal reference design or proof of hardware operation.

## Failure pattern

Early iterations optimized visible trace completion and DRC status without a
complete circuit/constraint model. That produced recognizable but inadequate
results: D+/D− were connected without remaining coupled, GND pads appeared
unconnected because useful filled planes were absent or stale, display highlight
colors were mistaken for layer/type, and an SMT USB-C footprint trapped VBUS so
ordinary vias violated manufacturing assumptions.

The underlying issue was not merely a CLI limitation. The workflow lacked a
study gate, exact metrics, filled-zone reconciliation, independent output review,
and a strict separation between CAD cleanliness and functional proof.

## Corrective design choices

- Expand the key matrix to 2×5 with one consistently oriented diode per key and
  a pin-for-pin QMK contract.
- Use ATmega32U4-AU at 5 V/16 MHz with all supply/ground pins, UCAP, local
  decoupling, clock, reset, and ISP accounted for from Microchip sources.
- Implement USB-C as a USB 2.0 sink with locally joined A/B data contacts and
  separate 5.1 kΩ CC1/CC2 pull-downs.
- Place a flow-through USB ESD device near the connector and preserve a coupled
  D+/D− main run through the required 22 Ω series resistors.
- Replace the USB4105 SMT connector with GCT USB4085-GF-A. Its plated-through
  signal/VBUS pins escape through ordinary traces and external vias, eliminating
  the earlier via-in-pad/VIPPO fabrication dependency.
- Put switches on the user side and all SMT on the underside. Treat the USB-C
  connector and ISP header as explicit later THT operations.
- Fill GND zones on both copper layers and reconcile expected GND pads against
  actual attachment state instead of trusting ratsnest disappearance.

## Verification achieved

The released source recorded zero native KiCad ERC violations, zero DRC
violations, zero unconnected items, and zero schematic-parity issues. A clean
jobset completed six jobs; KiBot produced zero unique warnings; Gerbv and
PyGerber independently parsed the manufacturing layers; the Gerber/drill archive
contained nine Gerbers plus separate PTH/NPTH drills; BOM/CPL, footprint geometry,
ground attachments, firmware pin contract, and archive hashes passed their
supplemental checks.

These results establish a design-checks-passed fabrication candidate. They do
not establish that an assembled board enumerates, flashes, scans all keys,
survives ESD, meets USB electrical compliance, or operates reliably. The case
study therefore retains an unexecuted bring-up plan.

## Generalizable lessons

1. Study exact devices and the intended production process before routing.
2. Turn every critical requirement into a rule or a named manual measurement.
3. Verify actual topology and return paths; trace color and total length are weak
   proxies.
4. Treat zones as generated geometry that must be refilled and audited.
5. Inspect the files sent to fabrication with another parser.
6. Model assembly process per component; “one board side” is not the same as one
   soldering process.
7. Preserve failures and source hashes so a successful retry is credible.
8. Reserve functional claims for physical measurements.

The complete sanitized source and evidence records are under
`examples/tenkey-macropad/`.
