# 🔬 PHYSICS — Références RATISS-ATELIER

## Flexion des poutres (Euler-Bernoulli)
- Flèche d'une console : δ = F·L³/(3·E·I), avec I = b·h³/12.
  Source : *Gere & Goodno, Mechanics of Materials, 9ᵉ éd., Cengage (2017)*.

## Propriétés matériaux (datasheets constructeurs)
| Matériau | E (GPa) | σy (MPa) | α (1/K) | T max (°C) |
|----------|:---:|:---:|:---:|:---:|
| PLA | 3.5 | 50 | 70e-6 | 60 |
| PETG | 2.1 | 53 | 60e-6 | 80 |
| ABS | 2.3 | 40 | 90e-6 | 98 |
| Aluminium | 69 | 276 | 23e-6 | 400 |
| Laiton | 100 | 250 | 19e-6 | 500 |

Sources : datasheets (NatureWorks PLA, etc.) + *CRC Handbook (2016)* + *Callister,
Materials Science and Engineering, Wiley (2018)*.

## Dilatation thermique
- ΔL = α·L·ΔT. Source : *Callister (2018)*.

## Fatigue thermique
- Modèle de Coffin-Manson simplifié : N_f ≈ (ε_limite/Δε)², Δε = α·ΔT.
  Source : *Coffin, "A study of the effects of cyclic thermal stresses...",
  Trans. ASME 76:931 (1954)*.

*RATIS Labs · Cameroun — constantes vérifiables.*
