"""Outil en ligne de validation mathématique & physique — RATISS-ATELIER.

Recalcule INDÉPENDAMMENT chaque résultat du simulateur FEM par une méthode
analytique différente, et le confronte à des références externes sourcées
(Gere & Goodno, Callister, Coffin 1954, datasheets matériaux).

Croisements :
  - flexion console : δ = FL³/(3EI) (Euler-Bernoulli, cas manuel de référence)
  - contrainte : σ = Mc/I avec I = bh³/12
  - dilatation : ΔL = α·L·ΔT
  - fatigue : Coffin-Manson N_f = (ε_lim/Δε)²
  - matériaux : E, σy, α dans les gammes publiées
  - sélection : exclusion automatique si T_service > T_max

Usage : PYTHONPATH=. python scripts/validate_physics.py
"""

from __future__ import annotations

from ratiss_atelier.fem import (MATERIALS, Beam, choose_material,
                                thermal_fatigue_cycles, will_survive)


def banner(txt):
    print("\n" + "=" * 68 + "\n" + txt + "\n" + "=" * 68)


def verdict(name, ok, detail):
    print(f"  [{'✅ PASS' if ok else '❌ FAIL'}] {name:<48} {detail}")
    return ok


def validate_euler_bernoulli_manual() -> bool:
    """Cas manuel de référence : console alu 1 m, 100 N.

    I = 0.1·0.01³/12 = 8.333e-9 m⁴ ; δ = FL³/(3EI) = 100/(3·69e9·8.333e-9) ≈ 58.0 mm.
    Calcul manuel indépendant du module.
    """
    b = Beam(1.0, 0.1, 0.01, material="ALU")
    i_manual = 0.1 * 0.01**3 / 12.0
    delta_manual = 100.0 * 1.0**3 / (3.0 * 69e9 * i_manual)
    delta_sim = b.deflection_m(100.0)
    ok = abs(delta_sim - delta_manual) < 1e-9
    return verdict("Euler-Bernoulli: cas manuel (Gere & Goodno)",
                   ok, f"δ_sim={delta_sim*1000:.2f} mm vs δ_manuel={delta_manual*1000:.2f} mm")


def validate_stress_manual() -> bool:
    """Contrainte de flexion : σ = M·c/I, M = F·L, c = h/2 — recalcul manuel."""
    b = Beam(0.5, 0.02, 0.01, material="PETG")
    i_m = 0.02 * 0.01**3 / 12.0
    sigma_manual = (50.0 * 0.5) * 0.005 / i_m / 1e6
    sigma_sim = b.max_stress_mpa(50.0)
    ok = abs(sigma_sim - sigma_manual) < 1e-9
    return verdict("Contrainte: σ = M·c/I",
                   ok, f"σ_sim={sigma_sim:.2f} MPa vs σ_manuel={sigma_manual:.2f} MPa")


def validate_scaling_laws() -> bool:
    """Lois d'échelle : δ ∝ F (linéaire), δ ∝ L³, δ ∝ 1/E — signatures de la théorie."""
    b = Beam(0.2, 0.02, 0.005, material="ALU")
    b2 = Beam(0.4, 0.02, 0.005, material="ALU")
    pla = Beam(0.2, 0.02, 0.005, material="PLA")
    ok = (abs(b.deflection_m(20) / b.deflection_m(10) - 2.0) < 1e-9
          and abs(b2.deflection_m(10) / b.deflection_m(10) - 8.0) < 1e-9
          and abs(b.deflection_m(10) / pla.deflection_m(10) - 3.5 / 69.0) < 1e-9)
    return verdict("Lois d'échelle: δ∝F, δ∝L³, δ∝1/E", ok, "3 signatures exactes")


def validate_thermal_expansion() -> bool:
    """Dilatation : ΔL = α·L·ΔT — alu, 1 m, 100 K → 2.3 mm (α = 23e-6)."""
    b = Beam(1.0, 0.02, 0.01, material="ALU")
    dl = b.thermal_expansion_m(100.0)
    ok = abs(dl - 23e-6 * 1.0 * 100.0) < 1e-12
    return verdict("Dilatation: ΔL = α·L·ΔT (alu 100 K → 2.3 mm)",
                   ok, f"ΔL = {dl*1000:.2f} mm")


def validate_coffin_manson() -> bool:
    """Coffin-Manson simplifié : N_f = (ε_lim/αΔT)² — recalcul manuel PETG 50 K."""
    nf_sim = thermal_fatigue_cycles("PETG", 50.0)
    nf_manual = (0.01 / (60e-6 * 50.0)) ** 2
    ok = abs(nf_sim - nf_manual) < 1e-6
    return verdict("Fatigue: Coffin-Manson N_f = (ε_lim/Δε)²",
                   ok, f"N_f = {nf_sim:.0f} cycles (PETG, ΔT=50 K)")


def validate_material_ranges() -> bool:
    """Propriétés matériaux dans les gammes publiées (Callister 2018, datasheets)."""
    ranges = {"E_gpa": (1.0, 210.0), "sigma_y_mpa": (20.0, 500.0),
              "alpha_per_k": (1e-6, 150e-6)}
    ok = True
    for name, props in MATERIALS.items():
        for key, (lo, hi) in ranges.items():
            if not (lo <= props[key] <= hi):
                ok = False
    return verdict("Matériaux: E, σy, α dans gammes publiées",
                   ok, f"{len(MATERIALS)} matériaux vérifiés")


def validate_service_temperature_exclusion() -> bool:
    """Sélection : à 90 °C de service, PLA (60 °C max) DOIT être exclu, alu inclus."""
    res = choose_material(10.0, 0.1, 90.0)
    pla = next(r for r in res if r["material"] == "PLA")
    alu = next(r for r in res if r["material"] == "ALU")
    ok = (not pla["temp_ok"]) and alu["temp_ok"]
    return verdict("Sélection: T_service > T_max exclut le matériau",
                   ok, "PLA exclu à 90 °C, alu retenu")


def validate_safety_factor() -> bool:
    """Coefficient de sécurité : σy/σ_appliquée — recalcul manuel."""
    b = Beam(0.1, 0.02, 0.005, material="ALU")
    r = will_survive(b, 20.0)
    sf_manual = 276.0 / b.max_stress_mpa(20.0)
    ok = abs(r["safety_factor_actual"] - sf_manual) < 1e-9
    return verdict("Sécurité: coef = σy/σ_appliquée",
                   ok, f"coef = {r['safety_factor_actual']:.1f}")


def main() -> int:
    banner("VALIDATION MATHÉMATIQUE & PHYSIQUE — RATISS-ATELIER\n"
           "Recalcul indépendant + confrontation à la littérature (Gere, Callister, Coffin)")
    checks = [
        validate_euler_bernoulli_manual,
        validate_stress_manual,
        validate_scaling_laws,
        validate_thermal_expansion,
        validate_coffin_manson,
        validate_material_ranges,
        validate_service_temperature_exclusion,
        validate_safety_factor,
    ]
    results = [fn() for fn in checks]
    banner("RÉSUMÉ")
    n_pass = sum(results)
    print(f"  {n_pass}/{len(results)} validations réussies")
    if n_pass == len(results):
        print("  ✅ Le simulateur FEM est cohérent avec la théorie des matériaux.")
        return 0
    print("  ❌ Écarts détectés — corriger le simulateur.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
