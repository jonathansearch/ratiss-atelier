# 🔧 ASSEMBLY — Guide de montage RATISS-ATELIER

Document exécutable par un technicien mécanicien/fabricant (ENSPY, Lycée
technique, diaspora). Chaque étape est vérifiable. **La sécurité machine
(arrêts d'urgence, carters, ventilation) est installée AVANT la première
mise sous tension.**

---

## ⚠️ Consignes de sécurité

- **Lunettes obligatoires** à chaque opération CNC — un copeau d'aluminium à
  12 000 tr/min ne prévient pas.
- **Arrêt d'urgence coup-de-poing** câblé en série sur l'alimentation de la
  broche ET des moteurs, testé avant le premier usinage.
- **Ventilation** : l'ABS émet des styrènes — extraction locale ou privilégier
  PLA/PETG. Jamais de combustion de chutes plastiques.
- La buse atteint 260 °C, le plateau 100 °C : **jamais de contact direct**,
  jamais d'impression sans surveillance pour les 3 premiers mois.

---

## 🖨️ A. Imprimante 3D FDM

### A.1 Cadre et mécanique
1. Assembler le cadre en profilés 2020 à équerres — **vérifier l'équerrage à
   l'équerre de mécanicien sur les 6 faces** (l'équerrage du cadre conditionne
   la précision de toutes les pièces futures).
2. Monter les axes (rails ou tiges), courroies GT2 tendues au « ping » (doivent
   résonner, pas pendre).
3. **Vérification** : chaque chariot coulisse sans point dur sur toute la course.

### A.2 Électronique et firmware
1. Câbler la carte contrôleur : moteurs, fins de course, hotend, plateau,
   ventilos — sertir les connecteurs, pas de soudure volante.
2. Flasher **Klipper** (recommandé, open-source) ou Marlin.
3. Régler les courants des drivers TMC au multimètre (V_ref selon datasheet).
4. **Vérification** : homing des 3 axes sans collision, chauffe buse + plateau
   à consigne ±2 °C.

### A.3 Calibration (la qualité se gagne ici)
1. Nivellement plateau (feuille de papier, 4 coins + centre).
2. Calibration des steps/mm (cube 20 mm : mesurer au pied à coulisse, ajuster).
3. Calibration du débit (tour à paroi simple).
4. **Pièce de réception** : cube de calibration → cotes ±0.1 mm exigées.
5. **Validation FEM croisée** : imprimer la console de test, la charger avec un
   poids connu, mesurer la flèche au comparateur et comparer à
   `Beam.deflection_m()` — écart documenté → recalibrer le module d'Young
   effectif du filament (les pièces imprimées sont ~30-50 % plus souples que
   le matériau brut, c'est physique : couches et remplissage).

---

## ⚙️ B. Fraiseuse CNC 3 axes

### B.1 Mécanique
1. Assembler le portique sur la table — **l'équerrage portique/table se mesure
   au comparateur**, pas à l'œil.
2. Régler le jeu des vis trapézoïdales (écrous anti-backlash).
3. **Vérification** : backlash < 0.05 mm mesuré au comparateur sur chaque axe.

### B.2 Broche et sécurité
1. Monter la broche 500 W, vérifier l'alignement de l'axe Z à l'équerre.
2. Câbler l'**arrêt d'urgence en série** (broche + moteurs), le tester 3 fois.
3. **Vérification** : coup de poing enfoncé → tout s'arrête en < 1 s.

### B.3 Premier usinage (alu 6061)
1. Paramètres de départ prudents : 12 000 tr/min, avance 300 mm/min, passe
   0.3 mm, lubrification (huile de coupe ou alcool).
2. Usiner un carré de test 40×40 → mesurer au pied à coulisse (±0.1 mm).
3. **Validation FEM croisée** : usiner la console alu de test, mesurer sa
   flèche sous charge, comparer à `Beam.deflection_m()` — pour l'alu plein,
   l'écart doit être < 15 % (sinon, vérifier la rigidité machine).

---

## 🔄 C. La boucle de fabrication RATISS

```
Concevoir (CAO) → Simuler (FEM in silico) → Fabriquer → Mesurer → Recalibrer
```

Pour **chaque pièce des priorités 0-3** :
1. Dessiner la pièce (FreeCAD/OpenSCAD — open-source).
2. La valider dans `ratiss_atelier.fem` : `will_survive`, dilatation,
   fatigue si elle voit des cycles thermiques.
3. Choisir le matériau avec `choose_material()` (température de service !).
4. Fabriquer, mesurer, comparer à la prédiction, documenter l'écart.
5. Recalibrer le modèle (E effectif du filament, rigidité réelle des pièces).

**On ne consomme de la matière que pour une pièce déjà validée.**

---

*RATIS Labs · Cameroun — Mesurer deux fois, couper une fois.*
