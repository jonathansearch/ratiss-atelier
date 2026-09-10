"""Génère le G-code de la console de test FEM (pièce de réception CNC).

La boucle RATISS complète : la FEM (ratiss_atelier.fem) valide la pièce,
ce script la transforme en instructions machine pour la CNC (GRBL/FluidNC).
La console rectangulaire de test est usinée dans de l'alu 6061, chargée,
mesurée au comparateur — et l'écart avec la prédiction recalibre le modèle.

G-code dialecte : GRBL 1.1 (unités mm, absolu G90, broche 12 000 tr/min).

Usage : PYTHONPATH=. python scripts/generate_gcode.py [--out results/console_test.gcode]
"""

from __future__ import annotations

import argparse
import os

from ratiss_atelier.fem import Beam, will_survive

# Paramètres d'usinage alu 6061 (prudents — ASSEMBLY §B.3)
SPINDLE_RPM = 12000
FEED_XY = 300.0        # mm/min
FEED_Z = 100.0         # mm/min
PASS_DEPTH = 0.3       # mm par passe
SAFE_Z = 5.0           # hauteur de sécurité


def gcode_console(length_mm: float, width_mm: float, thickness_mm: float,
                  stock_thickness_mm: float) -> str:
    """G-code : contour de la console + trou de fixation à l'encastrement.

    La pièce est détourée d'un brut par passes successives de 0.3 mm, puis un
    trou de fixation (M4) est percé à 10 mm de l'extrémité encastrée — c'est
    là que la contrainte est maximale (voir 07_carte_contrainte.png), le trou
    est donc placé dans la zone de moindre contrainte transverse (axe neutre).
    """
    lines = [
        "; RATISS-ATELIER — console de test FEM (alu 6061)",
        f"; dimensions : {length_mm}x{width_mm}x{thickness_mm} mm",
        "; validee par ratiss_atelier.fem avant fabrication",
        "G21        ; unites mm",
        "G90        ; coordonnees absolues",
        "G17        ; plan XY",
        f"M3 S{SPINDLE_RPM}   ; broche {SPINDLE_RPM} tr/min",
        "G4 P2      ; attendre regime broche",
        f"G0 Z{SAFE_Z}      ; hauteur de securite",
    ]
    # Détourage par passes de profondeur croissante
    depth = PASS_DEPTH
    z_target = stock_thickness_mm + 0.2  # traverser le brut + martyr
    while depth <= z_target:
        z = -min(depth, z_target)
        lines += [
            f"; --- passe a Z{z:.2f} ---",
            f"G0 X0 Y0",
            f"G1 Z{z:.2f} F{FEED_Z}",
            f"G1 X{length_mm:.2f} F{FEED_XY}",
            f"G1 Y{width_mm:.2f}",
            f"G1 X0",
            f"G1 Y0",
            f"G0 Z{SAFE_Z}",
        ]
        depth += PASS_DEPTH
    # Trou de fixation M4 (axe neutre, 10 mm de l'encastrement)
    lines += [
        "; trou de fixation M4 (axe neutre, zone de moindre contrainte)",
        f"G0 X10.00 Y{width_mm/2:.2f}",
        f"G1 Z{-z_target:.2f} F{FEED_Z}",
        f"G0 Z{SAFE_Z}",
        "M5         ; broche off",
        "G0 X0 Y0   ; retour origine",
        "M2         ; fin de programme",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(__file__), "..", "results", "console_test.gcode"))
    args = ap.parse_args()

    # La pièce DOIT être validée FEM avant de générer le G-code — c'est la
    # règle de l'atelier : on ne consomme de la matière que pour une pièce
    # déjà validée.
    beam = Beam(0.10, 0.02, 0.005, material="ALU")
    check = will_survive(beam, force_n=50.0, safety_factor=2.0)
    if not check["survives"]:
        print("❌ Pièce non validée FEM — pas de G-code. Revoir le dimensionnement.")
        return 1
    print(f"✅ Validation FEM : coef sécurité {check['safety_factor_actual']:.1f} "
          f"(requis 2.0), flèche sous 50 N : {beam.deflection_m(50)*1000:.2f} mm")

    gcode = gcode_console(length_mm=100.0, width_mm=20.0, thickness_mm=5.0,
                          stock_thickness_mm=5.0)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(gcode)
    n_passes = gcode.count("--- passe")
    print(f"✅ G-code généré : {args.out} ({n_passes} passes + trou M4, "
          f"{len(gcode.splitlines())} lignes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
