# Local Audit Report — ratiss-atelier

> Scope: local clone only. No remote repository was modified and no push was performed.

## Repository Structure

| Check | Result |
|---|---|
| Tracked/local file count | 38 |
| Python file count | 8 |
| README | PASS |
| RATISS Labs logo (`docs/assets/logo.png`) | PASS |
| Apache 2.0 LICENSE | PASS |
| `CITATION.cff` | PASS |

## Test Validation

- Command: `python3 -m pytest -v`
- Exit status: `0`

```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/ubuntu/ratiss-labs-repos/ratiss-atelier
configfile: pyproject.toml
plugins: anyio-4.14.2
collecting ... collected 14 items

tests/test_atelier.py::TestBeam::test_second_moment PASSED               [  7%]
tests/test_atelier.py::TestBeam::test_deflection_scales_with_force PASSED [ 14%]
tests/test_atelier.py::TestBeam::test_stiffer_material_deflects_less PASSED [ 21%]
tests/test_atelier.py::TestBeam::test_longer_beam_deflects_more PASSED   [ 28%]
tests/test_atelier.py::TestSurvival::test_alu_stronger_than_pla PASSED   [ 35%]
tests/test_atelier.py::TestSurvival::test_heavy_load_fails_pla PASSED    [ 42%]
tests/test_atelier.py::TestFatigue::test_bigger_dt_fewer_cycles PASSED   [ 50%]
tests/test_atelier.py::TestFatigue::test_low_expansion_material_last_longer PASSED [ 57%]
tests/test_atelier.py::TestMaterialChoice::test_returns_all_materials PASSED [ 64%]
tests/test_atelier.py::TestMaterialChoice::test_hot_service_excludes_pla PASSED [ 71%]
tests/test_atelier.py::TestFigures::test_all_figures_valid PASSED        [ 78%]
tests/test_atelier.py::TestPhysicsValidation::test_validate_physics_all_pass PASSED [ 85%]
tests/test_atelier.py::TestGCodeGeneration::test_gcode_well_formed PASSED [ 92%]
tests/test_atelier.py::TestGCodeGeneration::test_gcode_console_structure PASSED [100%]

============================== 14 passed in 8.40s ==============================

```

## Compliance Notes

- Branding and common repository metadata were applied locally.
- Scientific claims were not upgraded from proxy evidence to full validation.
- The three required technical Bible documents were not present in the supplied workspace.
- This report is an engineering audit snapshot, not a claim of zero defects.
