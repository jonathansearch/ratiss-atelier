"""RATISS-ATELIER — Atelier de fabrication souverain (Priorité 4).

Modélise les contraintes mécaniques/thermiques des pièces fabriquées
(impression 3D FDM, usinage CNC) par méthode des éléments finis simplifiée
(poutre/plaque) et prédit la tenue des pièces avant fabrication.

Objectif : valider in silico qu'un support de cristal photonique ne se déformera
pas sous la chaleur, ou qu'un bloc PCR ne fissurera pas après 1000 cycles
thermiques — avant de consommer du filament ou de l'aluminium.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# --- Propriétés matériaux (sourcées docs/PHYSICS.md) ---
# Module d'Young E (Pa), limite élastique σy (MPa), dilatation α (1/K)
MATERIALS = {
    "PLA":   {"E_gpa": 3.5,  "sigma_y_mpa": 50.0,  "alpha_per_k": 70e-6,  "t_max_c": 60.0},
    "PETG":  {"E_gpa": 2.1,  "sigma_y_mpa": 53.0,  "alpha_per_k": 60e-6,  "t_max_c": 80.0},
    "ABS":   {"E_gpa": 2.3,  "sigma_y_mpa": 40.0,  "alpha_per_k": 90e-6,  "t_max_c": 98.0},
    "ALU":   {"E_gpa": 69.0, "sigma_y_mpa": 276.0, "alpha_per_k": 23e-6,  "t_max_c": 400.0},
    "Laiton": {"E_gpa": 100.0, "sigma_y_mpa": 250.0, "alpha_per_k": 19e-6, "t_max_c": 500.0},
}


@dataclass
class Beam:
    """Poutre/console (modèle de flexion simple, Eulerr-Bernoulli).

    Représente un support de pièce (support d'optique, équerre, bras).
    """
    length_m: float
    width_m: float
    thickness_m: float
    material: str = "PETG"

    def props(self) -> dict:
        return MATERIALS[self.material]

    def second_moment_m4(self) -> float:
        """Moment quadratique I = b·h³/12 (section rectangulaire)."""
        return self.width_m * self.thickness_m**3 / 12.0

    def deflection_m(self, force_n: float) -> float:
        """Flèche en bout d'une console sous charge : δ = F·L³/(3·E·I)."""
        e_pa = self.props()["E_gpa"] * 1e9
        return force_n * self.length_m**3 / (3.0 * e_pa * self.second_moment_m4())

    def max_stress_mpa(self, force_n: float) -> float:
        """Contrainte max en flexion : σ = M·c/I avec M = F·L, c = h/2."""
        i_m4 = self.second_moment_m4()
        c = self.thickness_m / 2.0
        m = force_n * self.length_m
        return m * c / i_m4 / 1e6  # → MPa

    def thermal_expansion_m(self, delta_t_k: float) -> float:
        """Dilatation thermique : ΔL = α·L·ΔT."""
        return self.props()["alpha_per_k"] * self.length_m * delta_t_k


def will_survive(beam: Beam, force_n: float, safety_factor: float = 2.0) -> dict:
    """Vérifie qu'une pièce tient la charge avec un coefficient de sécurité."""
    sigma = beam.max_stress_mpa(force_n)
    sigma_y = beam.props()["sigma_y_mpa"]
    return {
        "stress_mpa": sigma,
        "yield_mpa": sigma_y,
        "safety_factor_actual": sigma_y / max(sigma, 1e-12),
        "safety_factor_required": safety_factor,
        "survives": bool(sigma_y / max(sigma, 1e-12) >= safety_factor),
    }


def thermal_fatigue_cycles(material: str, delta_t_k: float,
                           strain_limit: float = 0.01) -> float:
    """Cycles thermiques avant fatigue (modèle de Coffin-Manson simplifié).

    Δε_thermique = α·ΔT ; N_f ≈ (ε_limite / Δε)² — ordre de grandeur.
    """
    alpha = MATERIALS[material]["alpha_per_k"]
    d_eps = alpha * delta_t_k
    if d_eps <= 0:
        return float("inf")
    return float((strain_limit / d_eps) ** 2)


def choose_material(force_n: float, length_m: float, t_service_c: float,
                    safety_factor: float = 2.0) -> list:
    """Classe les matériaux par aptitude pour une pièce donnée."""
    results = []
    for name, props in MATERIALS.items():
        beam = Beam(length_m, 0.02, 0.005, material=name)
        chk = will_survive(beam, force_n, safety_factor)
        temp_ok = t_service_c < props["t_max_c"]
        results.append({
            "material": name,
            "survives": chk["survives"] and temp_ok,
            "safety_factor": chk["safety_factor_actual"],
            "temp_ok": temp_ok,
            "deflection_mm": beam.deflection_m(force_n) * 1000,
        })
    return sorted(results, key=lambda r: (not r["survives"], -r["safety_factor"]))
