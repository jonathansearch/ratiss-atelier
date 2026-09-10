# 🏭 RATISS-ATELIER — DOCUMENT DE CONCEPTION COMPLET

<div align="center">

![RATIS Labs](docs/images/05_logo_ratis_labs.png)

**L'atelier de fabrication souverain — Priorité 4 de la doctrine RATISS**

*RATIS Labs · Cameroun · Propriété : JOHNKING0 & Jonathan Evina · ORCID 0009-0000-4092-5313*

</div>

---

> 🇨🇲 **Un mot au Gouvernement de la République du Cameroun**
>
> Un support de cristal, un bloc de PCR : importés, ces composants coûtent des
> mois d'attente et des prix d'or. RATISS-ATELIER rend le Cameroun capable de
> fabriquer lui-même les pièces de ses instruments — imprimées en 3D ou usinées
> à la CNC, validées par simulation avant de consommer le moindre gramme de
> matière. **La souveraineté industrielle n'attend pas : elle se fabrique.**

---

## 📑 Sommaire
1. [Vue d'ensemble](#1-vue-densemble)
2. [Imprimante 3D FDM](#2-imprimante-3d)
3. [Fraiseuse CNC](#3-fraiseuse-cnc)
4. [Les machines montées](#4-les-machines-montées)
5. [Le simulateur FEM](#5-le-simulateur-fem)
6. [Choix des matériaux](#6-choix-des-matériaux)
7. [Carte de contrainte : où renforcer](#7-carte-de-contrainte--où-renforcer)
8. [Validation mathématique et physique](#8-validation)
9. [Coût et montage](#9-coût-et-montage)
10. [Itérations](#10-itérations)
11. [Sécurité](#11-sécurité)
12. [Feuille de route](#12-feuille-de-route)

---

## 1. Vue d'ensemble

RATISS-ATELIER est la **capacité de fabrication locale** : impression 3D (FDM)
et usinage CNC 3 axes, avec **validation FEM in silico** avant chaque
fabrication. Il produit les pièces mécaniques de toutes les autres priorités
RATISS (supports d'optique du QPU, blocs PCR du biolab, structure du cluster).

## 2. Imprimante 3D

![Plan imprimante](docs/images/01_plan_imprimante.png)

Architecture cartésienne (type Prusa i3 / Voron) : cadre aluminium extrudé,
moteurs NEMA17, courroies GT2, buse 0.4 mm, plateau chauffant. Précision ±0.1 mm
— suffisant pour boîtiers, supports et pièces plastiques.

## 3. Fraiseuse CNC

![Plan CNC](docs/images/02_plan_cnc.png)

Portique mobile, broche 500 W, vis trapézoïdales (±0.05 mm). Usine l'aluminium
et le laiton : blocs PCR (Priorité 2), supports de cristaux (Priorité 1), et
les pièces de précision introuvables localement.

## 4. Les machines montées

![Machines](docs/images/03_machines_montees.png)

## 5. Le simulateur FEM

`ratiss_atelier/fem.py` valide chaque pièce **avant** fabrication :

| Analyse | Modèle | Usage |
|---------|--------|-------|
| Flexion | Euler-Bernoulli δ = FL³/3EI | support tient-il la charge ? |
| Contrainte | σ = M·c/I | dépasse-t-on la limite élastique ? |
| Dilatation | ΔL = α·L·ΔT | la pièce se déforme-t-elle à chaud ? |
| Fatigue thermique | Coffin-Manson | combien de cycles avant fissure ? |

### De la validation à la machine : le G-code

`scripts/generate_gcode.py` boucle la chaîne : il **refuse de produire du
G-code pour une pièce non validée FEM**, puis génère les instructions GRBL de
la console de test (détourage par passes de 0.3 mm, trou de fixation M4 placé
sur l'axe neutre — la zone de moindre contrainte, voir §7). La pièce usinée est
chargée, mesurée au comparateur, et l'écart avec la prédiction recalibre le
modèle. **Simulation et fabrication ne font qu'un.**

## 6. Choix des matériaux

![FEM](docs/images/04_fem_validation.png)

`choose_material()` classe PLA / PETG / ABS / alu / laiton par aptitude pour une
pièce donnée (charge, température de service, coefficient de sécurité). La FEM
montre que l'aluminium fléchit ~20× moins que le PLA et résiste bien mieux à la
fatigue thermique — critique pour le bloc PCR qui subit 1000+ cycles.

![Choix matériau](docs/images/06_choix_materiau.png)

Le tableau de décision ci-dessus montre un cas réel : un support devant tenir
10 N à 90 °C (proximité du bloc PCR, Priorité 2). **La température de service
élimine PLA et PETG d'office** — leur limite thermique (60 °C / 80 °C) est sous
la consigne avant même qu'on parle de mécanique. Restent l'ABS (limite), l'alu
et le laiton. C'est le genre de piège qu'un achat à l'aveugle ne voit pas.

## 7. Carte de contrainte : où renforcer

![Carte contrainte](docs/images/07_carte_contrainte.png)

La contrainte de flexion d'une console suit σ(x) = F·(L−x)·c/I : **maximale à
l'encastrement, nulle au bout libre**. Conséquence pratique immédiate pour le
fabricant : c'est à la racine de la pièce qu'on ajoute de la matière (congés,
épaisseur, renfort), pas en extrémité. Une intuition fréquente (« renforcer là
où ça bouge ») est exactement fausse — la FEM la corrige avant d'avoir cassé
une pièce.

## 8. Validation

L'outil `scripts/validate_physics.py` **recalcule indépendamment** chaque
résultat FEM et le confronte à la littérature :

```
PYTHONPATH=. python scripts/validate_physics.py
→ 8/8 validations réussies ✅
```

- **Flexion** : cas manuel de référence (console alu 1 m, 100 N → 57.97 mm) —
  coïncidence exacte avec Gere & Goodno.
- **Contrainte** : σ = M·c/I recalculée à la main — exacte.
- **Lois d'échelle** : δ∝F, δ∝L³, δ∝1/E — trois signatures exactes de la
  théorie d'Euler-Bernoulli.
- **Dilatation** : ΔL = α·L·ΔT (alu 1 m, 100 K → 2.30 mm).
- **Fatigue** : Coffin-Manson N_f = (ε_lim/Δε)² recalculé.
- **Matériaux** : E, σy, α des 5 matériaux dans les gammes publiées (Callister).
- **Sélection** : exclusion automatique quand T_service > T_max.

> ⚠️ **Honnêteté sur la fatigue** : le PETG à ΔT = 50 K donne N_f ≈ 11 cycles —
> le modèle Coffin-Manson simplifié est **pessimiste** (il ignore l'élasticité
> réversible des polymères). On le garde volontairement : un dimensionnement
> pessimiste protège la pièce ; un optimiste la sacrifie.

## 9. Coût et montage

> 📦 **[BOM détaillée → docs/BOM.md](docs/BOM.md)** — ~759 k FCFA l'atelier
> complet, **~343 k pour l'imprimante 3D seule en phase 1** ; chaque machine
> autofinance la suivante en évitant les imports.
>
> 🔧 **[Guide de montage → docs/ASSEMBLY.md](docs/ASSEMBLY.md)** — équerrage au
> comparateur, calibration (steps/mm, débit), arrêt d'urgence testé, pièce de
> réception, boucle de recalibrage FEM sur mesures réelles.

## 10. Itérations

### Itération 1 : valider avant de fabriquer
- **Problème** : fabriquer à l'aveugle gaspille matière et temps sur des pièces
  qui cassent.
- **Solution** : FEM in silico systématique. Leçon : **on ne consomme de la
  matière que pour une pièce déjà validée**.

### Itération 2 : le PLA ne tient pas la chaleur
- **Problème** : un support en PLA près du bloc PCR se ramollit (T max 60 °C).
- **Solution** : `choose_material` exclut automatiquement les matériaux dont la
  T max est sous la température de service. Leçon : **la température de service
  élimine des matériaux avant même la contrainte mécanique**.

### Itération 3 : les pièces imprimées sont plus souples que la matière brute
- **Problème** : une console imprimée (remplissage 40 %) fléchit 30-50 % de
  plus que la prédiction du module d'Young brut.
- **Solution** : la procédure de réception (ASSEMBLY §A.3) mesure la flèche
  réelle d'une console de test et recalibre E effectif du filament. Leçon :
  **le modèle se soumet à la mesure, pas l'inverse**.

## 11. Sécurité

| Danger | Mitigation |
|--------|-----------|
| Buse 260 °C / plateau 100 °C | Ne jamais toucher en fonctionnement |
| Fraise CNC rotative (12 000 tr/min) | Carter fermé, arrêt d'urgence testé, lunettes |
| Fumées ABS (styrènes) | Extraction locale, privilégier PLA/PETG |
| Incendie (chauffes prolongées) | Extincteur ABC à portée, surveillance les 3 premiers mois |

## 12. Feuille de route

| Phase | Statut | Livrable |
|-------|:------:|----------|
| 1 — Simulateur FEM + sélection matériaux + G-code | ✅ FAIT | 14/14 tests, 8/8 validations |
| 2 — Documentation (BOM, ASSEMBLY, DESIGN) | ✅ FAIT | docs complètes |
| 3 — Imprimante 3D (phase 1) | 🔜 À FAIRE | ~343 k FCFA, produit les pièces P1-P3 |
| 4 — Recalibrage FEM sur pièces réelles | 🔮 FUTUR | E effectif filament mesuré |
| 5 — CNC (phase 2) | 🔮 FUTUR | blocs PCR et supports optiques usinés |

---

<div align="center">

**RATIS Labs · Cameroun** — *Toujours itérer, jamais figé.* 🦇🏭

![RATIS Labs](docs/images/05_logo_ratis_labs.png)

</div>
