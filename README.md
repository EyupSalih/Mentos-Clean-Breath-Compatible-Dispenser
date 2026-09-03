# Mentos Clean Breath Compatible V7 Dual‑Magazine Pocket Dispenser

> 3D-printable, spring-fed, dual-magazine pocket dispenser designed to fit **Mentos Clean Breath** tablets.  
> **30-tablet capacity (15 + 15)**, anti-jam cutoff shuttle, closed outer shell, removable magazines, single-button spring release, sliding bottom service cover and a hinged dust flap.

![V7 product overview](media/v7_product_poster.png)
![V7 product overview for TR](media/v7_product_poster_TR.png)

## Project status

**V7 — functional CAD release**

The current digital CAD audit reports **no critical rigid-body collisions in the tested assembly and motion states**.  
This is **not** a physical certification. Before relying on the device for everyday use, validate the real print tolerances, spring force, TPU behavior, tablet batch variation and food-contact suitability of the materials you choose.

Nominal tablet model used in CAD:

- Diameter: **11.2 mm**
- Thickness: **5.9 mm**
- Maximum design envelope used in checks: **Ø11.55 × 6.20 mm**

## Key features

- **30-tablet capacity** — two removable 15-tablet magazines
- **Spring + follower feed system** in each magazine
- **Double-J follower lock** so the magazines can be filled while the springs remain restrained
- **Single side release button** releases both magazine followers after the case is closed
- **Closed exterior shell** — no long follower slots on the outside
- **Dual-pocket cutoff shuttle** — blocks the feed openings while moving to reduce double-feeds/jams
- **Raised thumb tab** for easier left/right operation
- **Hinged output dust flap**
- **Full-width sliding bottom service cover** — routine refill does not require removing the top screws
- **TPU/silicone anti-rattle elements**
- STEP source geometry, printable STL files, assembly-state CAD, hardware references and audit files included

## How it works

1. Remove a magazine from the body.
2. Remove the TPU feed ring.
3. Use the refill push-twist tool to push the follower down and rotate it into the **double-J lock**.
4. Load **15 tablets**.
5. Reinstall the TPU feed ring.
6. Repeat for the second magazine.
7. Insert both magazines into the chassis **while their springs are still locked**.
8. Close the sliding bottom cover.
9. Press the recessed side button once; the internal common release bar unlocks both followers.
10. Move the top shuttle left or right to bring one tablet to the center output.
11. Open the dust flap and remove the tablet.
12. Return the shuttle to the center/feed position.

## Assembly video

A detailed X-ray-style assembly, refill and usage video is included:

**[Watch / download the V7 assembly video](media/V7_XRAY_assembly_fill_use_30fps.mp4)**

The video uses transparent/X-ray views where the outer shell would otherwise hide the internal mechanism.

## Repository structure

```text
.
├── README.md
├── README_TR.md
├── LICENSE.md
├── LICENSE-CAD.md
├── LICENSE-SOFTWARE
├── GITHUB_SETUP.md
├── ASSEMBLY_STATES/
│   ├── 01_COMPLETE_30_LOADED_RELEASED.step
│   ├── 02_CUTAWAY_INTERNALS.step
│   └── ...
├── STEP_parts/
│   ├── 01_lower_chassis_closed_shell.step
│   ├── 02_transfer_base_metering_deck.step
│   ├── 03_top_cap_real_screw_access.step
│   └── ...
├── STL_printable/
│   ├── 01_lower_chassis_closed_shell.stl
│   ├── 02_transfer_base_metering_deck.stl
│   ├── 03_top_cap_real_screw_access.stl
│   └── ...
├── REFERENCE_hardware/
├── AUDIT/
├── SOURCE/
└── media/
    ├── v7_product_poster.png
    └── V7_XRAY_assembly_fill_use_30fps.mp4
```

For the detailed Turkish mechanical description, see **[README_TR.md](README_TR.md)**.

## Main printable parts

| No. | Part | Suggested material | Qty |
|---:|---|---|---:|
| 01 | Lower chassis / closed shell | PETG / ASA | 1 |
| 02 | Transfer base / metering deck | PETG / ASA | 1 |
| 03 | Top cap | PETG / ASA | 1 |
| 04 | Left magazine | PETG / ASA | 1 |
| 05 | Right magazine | PETG / ASA | 1 |
| 06 | Double-stem follower | PETG / ASA | 2 |
| 07 | Feed ring | TPU | 2 |
| 08 | Dual-pocket cutoff shuttle | PETG / ASA | 1 |
| 09 | Common release bar | PETG / ASA | 1 |
| 10 | Side-button dust seal | TPU | 1 |
| 11 | Output dust flap | TPU | 1 |
| 12 | Sliding bottom outer cover | PETG / ASA | 1 |
| 13 | Bottom preload pad | TPU | 2 |
| 14 | Refill push-twist tool | PETG / ASA | 1 |

See `AUDIT/V7_BOM_TR.csv` for the full bill of materials and hardware references.

## Referenced hardware

The repository contains reference CAD for the hardware used by the design, including:

- 2 × main compression springs
- 1 × release-button return spring
- 4 × M2.5 countersunk screws
- 4 × M2.5 heat-set inserts
- M3 shuttle center detent ball plunger
- M3 bottom-cover detent ball plunger
- 1.5 mm food-grade silicone cord

**Reference CAD is dimensional guidance only.** Match the physical hardware you actually purchase and verify dimensions before printing the final parts.

## Printing and material notes

PETG or ASA is recommended for the main rigid parts. Flexible sealing/feed parts are designed around TPU-type behavior.

If this device will directly contact food/tablets:

- choose materials whose manufacturer documents suitability for your intended contact use,
- consider nozzle, printer and post-processing contamination,
- clean parts appropriately,
- do not assume that a material is food-safe solely because it is sold as PETG or TPU.

## CAD audit and limitations

Audit material is stored in `AUDIT/`.

The digital checks cover selected rigid-body collisions, assembly paths and motion states. They **cannot** fully predict:

- FDM dimensional error
- layer orientation strength
- wear after repeated cycling
- actual spring-force curve
- TPU Shore hardness differences
- tablet manufacturing variation
- long-term dust sealing
- real-world impact/drop behavior

Physical prototype testing remains necessary.

## Licensing

This repository uses **split licensing**:

- CAD, STEP/STL files, documentation, images and project media: **CC BY-NC-SA 4.0**
- Source code / utility scripts in `SOURCE/`: **MIT License**

See [LICENSE.md](LICENSE.md), [LICENSE-CAD.md](LICENSE-CAD.md) and [LICENSE-SOFTWARE](LICENSE-SOFTWARE).

The non-commercial restriction means the design files may not be used commercially under the CC license without separate permission from the rights holder.

## Trademark / affiliation disclaimer

**Mentos** and **Mentos Clean Breath** are trademarks of their respective owners.  
This is an **independent, unofficial compatibility project** and is not affiliated with, sponsored by, approved by or endorsed by Mentos or Perfetti Van Melle.

The product name is used only to identify the tablet format the design is intended to fit.

## Contributions and modifications

Issues, tolerance measurements, print results and mechanical improvements are welcome.

If you publish a modified version of the licensed CAD/design material, follow the attribution and ShareAlike requirements in `LICENSE-CAD.md`.

---

### Türkçe kısa özet

Bu repo, Mentos Clean Breath tabletleri için tasarlanmış **15 + 15 kapasiteli çift şarjörlü, yay beslemeli V7 cep dispenserinin** STEP/STL dosyalarını, montaj durumlarını, audit dosyalarını ve detaylı X-ray montaj videosunu içerir. Ayrıntılı Türkçe teknik açıklama için **[README_TR.md](README_TR.md)** dosyasına bakın.
