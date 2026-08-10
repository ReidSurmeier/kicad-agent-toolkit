# Rev A fabrication notes

**Release claim:** CAD checks passed. These notes do not certify an unbuilt board. Obtain a fabricator DFM response before ordering.

## Board order

- Finished outline: **101.0 mm × 73.0 mm**, rectangular, coordinates `(2,2)` through `(103,75)` mm in the KiCad datum.
- Two copper layers, FR-4, finished thickness **1.60 mm ±10%**, **1 oz (35 µm) finished copper** on both sides.
- ENIG finish recommended for the USB connector, fine-pitch MCU, and exposed test pads; lead-free process.
- Minimum routed trace/space: **0.200/0.200 mm**. Power traces: **0.381 mm minimum**. Minimum finished drill: **0.300 mm**.
- Board-level hole-to-copper clearance: **0.250 mm**. The only smaller copper spacing is the connector-manufacturer land pattern described below.
- Four unplated 2.2 mm M2 clearance holes at `(5,5)`, `(100,5)`, `(5,72)`, `(100,72)` mm.
- Solder mask and paste are defined by the supplied Gerbers. Tent ordinary routing vias where the selected service allows.
- Do not infer a controlled-impedance claim. The 0.20/0.20 mm USB geometry is short full-speed USB routing on a two-layer board; no impedance-controlled stackup has been ordered or validated.

## USB4085 connector land pattern

J1 is the GCT `USB4085-GF-A`, a right-angle, through-hole USB 2.0 Type-C receptacle. Its four VBUS contacts and all other signal contacts are plated through-hole pins. The nearest layer transitions are ordinary external 0.30 mm drill / 0.60 mm pad vias; **there are no vias inside J1 pads and no VIPPO process is required**.

The stock KiCad-10 `Connector_USB:USB_C_Receptacle_GCT_USB4085` footprint follows the [GCT USB4085 drawing](https://gct.co/files/drawings/usb4085.pdf). Its 0.85 mm contact pitch and 0.70 mm PTH pads yield 0.150 mm adjacent-pad copper spacing. A custom rule permits 0.150 mm **only when both copper items belong to J1**. Global routed-copper clearance remains 0.200 mm and global hole-to-copper clearance remains 0.250 mm. Do not enlarge connector pads or drills without rechecking the manufacturer drawing.

## Assembly and panelization

- This revision uses **underside-only SMT assembly**. Every populated SMT part is on B.Cu; the front/user side carries only the ten through-hole MX switch bodies. J1 is a through-hole connector installed with its body on the underside and requires wave/selective/manual soldering after SMT reflow. J2 and the switches are also installed after underside reflow and optical inspection.
- The assembly house must generate/use the bottom-side stencil and bottom-side placement data. Do not mirror the supplied coordinates a second time; honor the side/rotation fields in the CPL and confirm them in the assembly viewer.
- Panel rails, tooling holes, fiducials, breakaways, and coupon strategy are the contract manufacturer's responsibility; none are inside the finished outline.
- No enclosure or switch plate is included. The selected exact switches are PCB-mount CHERRY MX parts; plate fit has not been claimed.
- The fabrication ZIP contains only the nine Gerbers and separate PTH/NPTH drill files. IPC-D-356 and IPC-2581 files are supplemental netlist/DFM exchange evidence, not substitutes for the Gerbers.
