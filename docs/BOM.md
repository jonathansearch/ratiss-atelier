# 📦 BOM — Bill of Materials RATISS-ATELIER (imprimante 3D + CNC)

Prix estimés FCFA. Privilégier les kits documentés open-source (Voron, Prusa,
PrintNC) — leurs plans sont publics et leurs pièces standard.

**Objectif : l'atelier complet < 500 000 FCFA**, et il produit ensuite les
pièces des 4 autres priorités RATISS — c'est un investissement multiplicateur.

---

## 🖨️ Imprimante 3D FDM (core XY ou cartésienne, volume 300³)

| # | Composant | Référence | Qté | PU (FCFA) | Total | Source |
|---|-----------|-----------|:---:|:---:|:---:|--------|
| 1 | Kit mécanique (profilés alu 2020, vis, roulements) | kit Voron Trident/Prusa | 1 | 90 000 | 90 000 | Chine |
| 2 | Moteurs pas-à-pas NEMA17 | 42-48 N·cm | 6 | 5 000 | 30 000 | Chine |
| 3 | Carte contrôleur 32 bits + drivers TMC2209 | BTT Octopus / SKR | 1 | 35 000 | 35 000 | Chine |
| 4 | Extrudeur + hotend all-metal | Orbiter / Dragon | 1 | 30 000 | 30 000 | Chine |
| 5 | Plateau chauffant 310×310 + lit PEI | 24 V | 1 | 25 000 | 25 000 | Chine |
| 6 | Alimentation 24 V 350 W | Mean Well | 1 | 18 000 | 18 000 | Dubaï |
| 7 | Raspberry Pi (Klipper) ou écran TFT | Pi 3/4 recyclé possible | 1 | 25 000 | 25 000 | local/récup |
| 8 | Filament PETG (5 kg) + PLA (5 kg) | 1.75 mm | 10 kg | 9 000 | 90 000 | Chine/Dubaï |

**Sous-total imprimante 3D : ~343 000 FCFA** (filament inclus pour démarrer)

---

## ⚙️ Fraiseuse CNC 3 axes (format 600×400, broche 500 W)

| # | Composant | Référence | Qté | PU (FCFA) | Total | Source |
|---|-----------|-----------|:---:|:---:|:---:|--------|
| 9 | Kit mécanique CNC (profilés, vis trapézoïdales, écrous) | PrintNC / WorkBee | 1 | 120 000 | 120 000 | Chine |
| 10 | Moteurs NEMA23 | 3 N·m | 4 | 12 000 | 48 000 | Chine |
| 11 | Broche 500 W ER11 + driver | 48 V | 1 | 45 000 | 45 000 | Chine |
| 12 | Carte contrôleur GRBL / FluidNC | ESP32 6-pack ou clone | 1 | 30 000 | 30 000 | Chine |
| 13 | Alimentation 48 V 500 W | Mean Well | 1 | 22 000 | 22 000 | Dubaï |
| 14 | Fraises carbure (assortiment alu) | 1/4" & 1/8" | 1 jeu | 25 000 | 25 000 | Chine |
| 15 | Brut aluminium 6061 (plaques + barres) | stock de départ | 1 lot | 40 000 | 40 000 | local/Dubaï |

**Sous-total CNC : ~330 000 FCFA**

---

## 🛡️ Sécurité & atelier commun

| # | Composant | Qté | PU (FCFA) | Total |
|---|-----------|:---:|:---:|:---:|
| 16 | Lunettes de protection + gants cuir | 2 | 5 000 | 10 000 |
| 17 | Arrêt d'urgence coup-de-poing (CNC) | 2 | 3 000 | 6 000 |
| 18 | Extincteur poudre ABC 6 kg | 1 | 25 000 | 25 000 |
| 19 | Aspiration copeaux (aspirateur d'atelier) | 1 | 30 000 | 30 000 |
| 20 | Ventilation locale (extraction ABS) | 1 | 15 000 | 15 000 |

**Sous-total sécurité : ~86 000 FCFA** — non négociable.

---

## 💰 Total projet

| Poste | Coût (FCFA) |
|-------|:---:|
| Imprimante 3D + filament | ~343 000 |
| CNC + bruts alu | ~330 000 |
| Sécurité atelier | ~86 000 |
| **TOTAL** | **~759 000** |

> 💡 **Découpage par phases** : l'imprimante 3D seule (~343 k) produit déjà les
> boîtiers, supports et plaques du cluster HPC (Priorité 3). La CNC vient en
> phase 2 pour les blocs PCR (Priorité 2) et les supports optiques (Priorité 1).
> Chaque machine autofinance la suivante en évitant des imports.

### Ce que l'atelier évite d'importer (retour sur investissement)

| Pièce produite localement | Prix importé (FCFA) | Coût local (matière) |
|---------------------------|:---:|:---:|
| Bloc PCR alu usiné (Priorité 2) | ~80 000 | ~8 000 |
| Support de cristal optique (Priorité 1) | ~50 000 | ~2 000 (PETG) |
| Plaques rack cluster (Priorité 3) ×8 | ~30 000 | ~4 000 |
| Boîtier incubateur (Priorité 2) | ~25 000 | ~6 000 |

---

*RATIS Labs · Cameroun — La machine qui fabrique les machines.*
