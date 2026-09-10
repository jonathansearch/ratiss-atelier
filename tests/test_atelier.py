"""Tests RATISS-ATELIER — FEM, matériaux, fatigue thermique."""

from ratiss_atelier.fem import (MATERIALS, Beam, choose_material,
                                thermal_fatigue_cycles, will_survive)


class TestBeam:
    def test_second_moment(self):
        b = Beam(0.1, 0.02, 0.005)
        assert abs(b.second_moment_m4() - 0.02 * 0.005**3 / 12) < 1e-15

    def test_deflection_scales_with_force(self):
        b = Beam(0.1, 0.02, 0.005, material="PETG")
        assert abs(b.deflection_m(20) - 2 * b.deflection_m(10)) < 1e-12

    def test_stiffer_material_deflects_less(self):
        pla = Beam(0.1, 0.02, 0.005, material="PLA")
        alu = Beam(0.1, 0.02, 0.005, material="ALU")
        assert alu.deflection_m(10) < pla.deflection_m(10)

    def test_longer_beam_deflects_more(self):
        short = Beam(0.05, 0.02, 0.005, material="PETG")
        long_ = Beam(0.20, 0.02, 0.005, material="PETG")
        # δ ∝ L³ → ×64 pour ×4 en longueur (0.05 → 0.20 m)
        assert abs(long_.deflection_m(10) / short.deflection_m(10) - 64.0) < 0.01


class TestSurvival:
    def test_alu_stronger_than_pla(self):
        pla = will_survive(Beam(0.1, 0.02, 0.005, "PLA"), 100)
        alu = will_survive(Beam(0.1, 0.02, 0.005, "ALU"), 100)
        assert alu["safety_factor_actual"] > pla["safety_factor_actual"]

    def test_heavy_load_fails_pla(self):
        assert not will_survive(Beam(0.2, 0.01, 0.003, "PLA"), 500)["survives"]


class TestFatigue:
    def test_bigger_dt_fewer_cycles(self):
        assert thermal_fatigue_cycles("PETG", 60) < thermal_fatigue_cycles("PETG", 30)

    def test_low_expansion_material_last_longer(self):
        # l'alu (α faible) résiste mieux à la fatigue thermique que le PLA
        assert thermal_fatigue_cycles("ALU", 50) > thermal_fatigue_cycles("PLA", 50)


class TestMaterialChoice:
    def test_returns_all_materials(self):
        assert len(choose_material(10, 0.1, 50)) == len(MATERIALS)

    def test_hot_service_excludes_pla(self):
        # à 90 °C, le PLA (Tmax 60) doit être exclu
        res = choose_material(10, 0.1, 90)
        pla = next(r for r in res if r["material"] == "PLA")
        assert not pla["temp_ok"]


class TestFigures:
    def test_all_figures_valid(self, tmp_path):
        import scripts.generate_figures as g
        g.OUT = str(tmp_path)
        g.fig_plan_imprimante(); g.fig_plan_cnc(); g.fig_machines_montees()
        g.fig_fem(); g.fig_choix_materiau(); g.fig_carte_contrainte(); g.fig_logo()
        for n in ["01_plan_imprimante.png", "02_plan_cnc.png",
                  "03_machines_montees.png", "04_fem_validation.png",
                  "06_choix_materiau.png", "07_carte_contrainte.png",
                  "05_logo_ratis_labs.png"]:
            p = tmp_path / n
            assert p.exists() and p.stat().st_size > 1000


class TestPhysicsValidation:
    def test_validate_physics_all_pass(self):
        import scripts.validate_physics as v
        assert v.main() == 0


class TestGCodeGeneration:
    def test_gcode_well_formed(self, tmp_path):
        import scripts.generate_gcode as g
        out = str(tmp_path / "console.gcode")
        import sys
        argv = sys.argv
        sys.argv = ["generate_gcode.py", "--out", out]
        try:
            assert g.main() == 0
        finally:
            sys.argv = argv
        with open(out) as f:
            content = f.read()
        # GRBL : unités mm, absolu, broche, fin de programme
        assert "G21" in content and "G90" in content
        assert "M3 S12000" in content and "M2" in content
        # passes de 0.3 mm jusqu'à traverser le brut 5 mm
        assert "Z-5.20" in content
        # trou de fixation sur l'axe neutre (Y = largeur/2 = 10 mm)
        assert "X10.00 Y10.00" in content

    def test_gcode_console_structure(self):
        import scripts.generate_gcode as g
        gcode = g.gcode_console(100.0, 20.0, 5.0, 5.0)
        lines = gcode.strip().split("\n")
        assert lines[0].startswith("; RATISS-ATELIER")
        assert lines[-1].startswith("M2")
        # chaque passe remonte en sécurité avant la suivante
        assert gcode.count("G0 Z5.0") >= gcode.count("--- passe")
