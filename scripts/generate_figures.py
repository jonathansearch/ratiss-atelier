"""Génère les figures RATISS-ATELIER : plans, machines, FEM, logo."""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "images")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"figure.dpi": 110, "font.size": 11,
                     "axes.grid": True, "grid.alpha": 0.3})

RATIS_DARK = "#0b1f3a"; RATIS_GREEN = "#1f9d55"; RATIS_GOLD = "#e0a800"
RATIS_RED = "#c0392b"; RATIS_BLUE = "#4aa3df"


def save(fig, name, facecolor="white"):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", facecolor=facecolor)
    plt.close(fig)
    print("généré :", name)


def _box(ax, x, y, w, h, text, fc, fs=8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                facecolor=fc, edgecolor=RATIS_DARK, linewidth=1.5, zorder=2))
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=fs, zorder=3,
            fontweight="bold")


# 1. PLAN IMPRIMANTE 3D
def fig_plan_imprimante():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 11); ax.set_ylim(0, 7); ax.axis("off")
    ax.set_title("PLAN DE CONCEPTION — Imprimante 3D FDM (type Prusa i3 / Voron)\n"
                 "Architecture cartésienne, filament PLA/PETG/ABS",
                 fontsize=12.5, fontweight="bold", color=RATIS_DARK)

    # Cadre
    ax.add_patch(Rectangle((1.5, 0.8), 0.3, 5.0, facecolor="#555", zorder=1))
    ax.add_patch(Rectangle((8.2, 0.8), 0.3, 5.0, facecolor="#555", zorder=1))
    ax.add_patch(Rectangle((1.5, 5.5), 7.0, 0.3, facecolor="#555", zorder=1))
    # Axe X + extrudeur
    ax.add_patch(Rectangle((1.8, 4.2), 6.4, 0.2, facecolor="#888", zorder=2))
    _box(ax, 4.6, 3.6, 0.8, 1.0, "Extru-\ndeur", RATIS_GOLD, 8)
    ax.add_patch(Rectangle((4.9, 3.2), 0.2, 0.4, facecolor=RATIS_RED, zorder=3))
    ax.text(5.0, 3.35, "buse", ha="center", fontsize=6, color="white", zorder=4)
    # Plateau
    ax.add_patch(Rectangle((2.0, 1.3), 6.0, 0.35, facecolor=RATIS_BLUE, zorder=2))
    ax.text(5.0, 1.47, "Plateau chauffant (axe Y)", ha="center", fontsize=8,
            color="white", zorder=3)
    # Filament
    ax.add_patch(Circle((9.8, 5.0), 0.7, facecolor="#eee", edgecolor=RATIS_DARK,
                        linewidth=2, zorder=2))
    ax.text(9.8, 5.0, "bobine", ha="center", fontsize=8, zorder=3)
    ax.annotate("", xy=(5.4, 4.3), xytext=(9.2, 5.0),
                arrowprops=dict(arrowstyle="->", color=RATIS_GREEN, lw=2))
    # axes
    ax.annotate("", xy=(8.2, 5.2), xytext=(8.2, 4.6),
                arrowprops=dict(arrowstyle="<->", color=RATIS_DARK, lw=1.5))
    ax.text(8.35, 4.9, "Z", fontsize=10, fontweight="bold")

    ax.text(0.5, 0.3,
            "CONCEPTION : cadre aluminium extrudé (rigide), moteurs NEMA17, courroies GT2.\n"
            "Buse 0.4 mm, plateau chauffant (ABS). Précision ±0.1 mm — suffisant pour les\n"
            "supports d'optique, boîtiers et pièces mécaniques des autres priorités RATISS.",
            fontsize=8.5, style="italic",
            bbox=dict(boxstyle="round", facecolor="#fffbe6", edgecolor=RATIS_GOLD))
    save(fig, "01_plan_imprimante.png")


# 2. PLAN CNC
def fig_plan_cnc():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 11); ax.set_ylim(0, 7); ax.axis("off")
    ax.set_title("PLAN DE CONCEPTION — Fraiseuse CNC 3 axes (alu, laiton, plastiques)\n"
                 "Portique mobile, broche 500 W, pas de vis trapézoïdales",
                 fontsize=12.5, fontweight="bold", color=RATIS_DARK)

    # Table
    ax.add_patch(Rectangle((1.0, 1.0), 8.0, 1.0, facecolor="#777", zorder=1))
    ax.text(5.0, 1.5, "Table de travail (martyr)", ha="center", fontsize=9,
            color="white", zorder=2)
    # Portique
    ax.add_patch(Rectangle((1.5, 2.0), 0.4, 3.5, facecolor="#555", zorder=1))
    ax.add_patch(Rectangle((8.1, 2.0), 0.4, 3.5, facecolor="#555", zorder=1))
    ax.add_patch(Rectangle((1.5, 5.0), 7.0, 0.5, facecolor="#555", zorder=1))
    ax.text(5.0, 5.25, "Portique (axe X)", ha="center", fontsize=9, color="white",
            zorder=2)
    # Broche
    _box(ax, 4.5, 3.8, 1.0, 1.2, "Broche\n500 W", RATIS_GOLD, 8)
    ax.add_patch(Rectangle((4.85, 2.3), 0.3, 1.5, facecolor=RATIS_RED, zorder=3))
    ax.text(5.0, 3.0, "fraise", ha="center", fontsize=6, color="white",
            rotation=90, zorder=4)
    # pièce
    ax.add_patch(Rectangle((4.2, 2.0), 1.6, 0.3, facecolor=RATIS_BLUE, zorder=2))
    ax.text(5.0, 2.15, "pièce alu", ha="center", fontsize=7, color="white", zorder=3)

    ax.text(0.5, 0.3,
            "CONCEPTION : vis à billes ou trapézoïdales (précision ±0.05 mm), broche 500 W\n"
            "pour aluminium et laiton. Usine les blocs PCR (Priorité 2), les supports de\n"
            "cristaux (Priorité 1) et les pièces de précision introuvables localement.",
            fontsize=8.5, style="italic",
            bbox=dict(boxstyle="round", facecolor="#fffbe6", edgecolor=RATIS_GOLD))
    save(fig, "02_plan_cnc.png")


# 3. MACHINES MONTÉES
def fig_machines_montees():
    fig, axs = plt.subplots(1, 2, figsize=(13, 6.5))
    fig.suptitle("RATISS-ATELIER — L'atelier souverain une fois monté",
                 fontsize=13, fontweight="bold", color=RATIS_DARK)

    # Imprimante 3D
    ax = axs[0]; ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.set_title("Imprimante 3D FDM", fontsize=11, fontweight="bold", color=RATIS_DARK)
    ax.add_patch(Rectangle((2.0, 1.5), 6, 7, facecolor="none",
                           edgecolor=RATIS_DARK, linewidth=3))
    ax.add_patch(Rectangle((2.6, 6.5), 4.8, 0.3, facecolor="#888"))
    ax.add_patch(Rectangle((4.4, 5.5), 1.2, 1.2, facecolor=RATIS_GOLD,
                           edgecolor=RATIS_DARK))
    ax.add_patch(Rectangle((2.6, 2.2), 4.8, 0.4, facecolor=RATIS_BLUE))
    # pièce en cours d'impression
    ax.add_patch(Rectangle((4.2, 2.6), 1.6, 1.4, facecolor=RATIS_GREEN,
                           edgecolor=RATIS_DARK, alpha=0.8))
    ax.text(5.0, 3.3, "pièce", ha="center", fontsize=8, color="white",
            fontweight="bold")
    ax.text(5.0, 0.8, "Impression en cours...", ha="center", fontsize=9,
            style="italic", color=RATIS_DARK)

    # CNC
    ax = axs[1]; ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.set_title("Fraiseuse CNC 3 axes", fontsize=11, fontweight="bold", color=RATIS_DARK)
    ax.add_patch(Rectangle((1.5, 1.5), 7, 1.2, facecolor="#666",
                           edgecolor=RATIS_DARK, linewidth=2))
    ax.add_patch(Rectangle((2.0, 2.7), 0.5, 4.0, facecolor="#555"))
    ax.add_patch(Rectangle((7.5, 2.7), 0.5, 4.0, facecolor="#555"))
    ax.add_patch(Rectangle((2.0, 6.3), 6.0, 0.5, facecolor="#555"))
    ax.add_patch(Rectangle((4.3, 4.8), 1.4, 1.5, facecolor=RATIS_GOLD,
                           edgecolor=RATIS_DARK))
    ax.add_patch(Rectangle((4.9, 3.0), 0.2, 1.8, facecolor=RATIS_RED))
    ax.add_patch(Rectangle((4.0, 2.7), 2.0, 0.3, facecolor=RATIS_BLUE))
    # copeaux
    rng = np.random.default_rng(1)
    ax.scatter(4.5+rng.random(15)*1.0, 3.1+rng.random(15)*0.4, s=8,
               color="#ccc", zorder=3)
    ax.text(5.0, 0.8, "Usinage alu en cours...", ha="center", fontsize=9,
            style="italic", color=RATIS_DARK)

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    save(fig, "03_machines_montees.png")


# 4. ANALYSE FEM
def fig_fem():
    from ratiss_atelier.fem import Beam, MATERIALS, thermal_fatigue_cycles
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.5))
    fig.suptitle("RATISS-ATELIER — Validation FEM : tenue mécanique & fatigue thermique",
                 fontsize=12.5, fontweight="bold", color=RATIS_DARK)

    # Flèche vs force pour chaque matériau
    forces = np.linspace(0, 50, 50)
    for mat, col in [("PLA", RATIS_GREEN), ("PETG", RATIS_GOLD),
                     ("ABS", RATIS_RED), ("ALU", RATIS_BLUE)]:
        b = Beam(0.10, 0.02, 0.005, material=mat)
        fl = [b.deflection_m(f)*1000 for f in forces]
        axs[0].plot(forces, fl, lw=2, color=col, label=mat)
    axs[0].set_xlabel("force (N)"); axs[0].set_ylabel("flèche (mm)")
    axs[0].set_title("Flexion d'une console 100 mm (Euler-Bernoulli)")
    axs[0].legend(fontsize=8)

    # Cycles de fatigue thermique
    dts = np.linspace(10, 80, 50)
    for mat, col in [("PLA", RATIS_GREEN), ("PETG", RATIS_GOLD), ("ALU", RATIS_BLUE)]:
        cyc = [min(thermal_fatigue_cycles(mat, dt), 1e5) for dt in dts]
        axs[1].plot(dts, cyc, lw=2, color=col, label=mat)
    axs[1].set_yscale("log")
    axs[1].axhline(1000, color="#888", linestyle="--", label="1000 cycles (bloc PCR)")
    axs[1].set_xlabel("ΔT par cycle (K)"); axs[1].set_ylabel("cycles avant fatigue")
    axs[1].set_title("Fatigue thermique (Coffin-Manson simplifié)")
    axs[1].legend(fontsize=8)

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    save(fig, "04_fem_validation.png")


# 5. SÉLECTION DE MATÉRIAU (tableau de décision)
def fig_choix_materiau():
    from ratiss_atelier.fem import choose_material, MATERIALS
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.5))
    fig.suptitle("RATISS-ATELIER — sélection de matériau pour un support chauffant (90 °C, 10 N)",
                 fontsize=12.5, fontweight="bold", color=RATIS_DARK)

    # Facteur de sécurité par matériau (service 90 °C)
    res = choose_material(10.0, 0.1, 90.0)
    names = [r["material"] for r in res]
    sf = [min(r["safety_factor"], 40) for r in res]
    cols = [RATIS_GREEN if r["survives"] else RATIS_RED for r in res]
    axs[0].bar(names, sf, color=cols)
    axs[0].axhline(2.0, color="black", linestyle="--", label="coef requis (2×)")
    for i, (r, v) in enumerate(zip(res, sf)):
        lbl = "OK" if r["survives"] else ("T° !" if not r["temp_ok"] else "faible")
        axs[0].text(i, v + 0.5, lbl, ha="center", fontsize=8, fontweight="bold")
    axs[0].set_ylabel("coefficient de sécurité"); axs[0].legend(fontsize=8)
    axs[0].set_title("Tenue mécanique + thermique (10 N, 90 °C)")

    # Limites de température vs service
    mats = list(MATERIALS)
    tmax = [MATERIALS[m]["t_max_c"] for m in mats]
    axs[1].barh(mats, tmax, color=[RATIS_GOLD, RATIS_GREEN, RATIS_BLUE,
                                   RATIS_RED, "#8e44ad"][:len(mats)])
    axs[1].axvline(90, color="black", lw=2, linestyle="--",
                   label="service bloc PCR (90 °C)")
    for i, v in enumerate(tmax):
        axs[1].text(v + 5, i, f"{v} °C", va="center", fontsize=8, fontweight="bold")
    axs[1].set_xlabel("température max de service (°C)"); axs[1].legend(fontsize=8)
    axs[1].set_title("Le PLA et l'ABS sont exclus d'office près du bloc PCR")

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    save(fig, "06_choix_materiau.png")


# 6. CARTE DE CONTRAINTE LE LONG D'UNE CONSOLE
def fig_carte_contrainte():
    from ratiss_atelier.fem import Beam
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.suptitle("RATISS-ATELIER — contrainte de flexion le long d'une console",
                 fontsize=12.5, fontweight="bold", color=RATIS_DARK)

    L, F = 0.20, 30.0
    x = np.linspace(0, L, 200)
    # σ(x) = F·(L−x)·c/I : max à l'encastrement, nulle en bout
    for mat, col in [("PETG", RATIS_GOLD), ("ALU", RATIS_BLUE)]:
        b = Beam(L, 0.02, 0.005, material=mat)
        i_m4 = b.second_moment_m4()
        c = 0.005 / 2
        sigma = F * (L - x) * c / i_m4 / 1e6
        ax.plot(x * 1000, sigma, lw=2.5, color=col,
                label=f"σ(x) — {mat}")
        ax.axhline(b.props()["sigma_y_mpa"], color=col, linestyle="--", alpha=0.6,
                   label=f"σy {mat} = {b.props()['sigma_y_mpa']:.0f} MPa")
    ax.annotate("zone critique :\nl'encastrement", xy=(0, 225), xytext=(30, 260),
                fontsize=9, color=RATIS_RED,
                arrowprops=dict(arrowstyle="->", color=RATIS_RED))
    ax.set_xlabel("position le long de la poutre (mm)")
    ax.set_ylabel("contrainte (MPa)")
    ax.set_title("σ(x) = F·(L−x)·c/I : c'est à l'encastrement qu'on renforce, pas en bout",
                 fontsize=10)
    ax.legend(fontsize=9)
    save(fig, "07_carte_contrainte.png")


# 7. LOGO
def fig_logo():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    fig.patch.set_facecolor(RATIS_DARK); ax.set_facecolor(RATIS_DARK)
    for angle, col in [(0, RATIS_GREEN), (60, RATIS_GOLD), (120, RATIS_BLUE)]:
        th = np.linspace(0, 2*np.pi, 200)
        x = 3.2*np.cos(th); y = 1.2*np.sin(th); a = np.radians(angle)
        xr = x*np.cos(a) - y*np.sin(a); yr = x*np.sin(a) + y*np.cos(a)
        ax.plot(5+xr, 5.6+yr, color=col, lw=3, alpha=0.9)
    ax.add_patch(Circle((5, 5.6), 0.7, facecolor=RATIS_GOLD, edgecolor="white",
                        linewidth=2, zorder=5))
    ax.text(5, 3.4, "RATIS LABS", ha="center", va="center", fontsize=34,
            fontweight="bold", color="white", family="sans-serif")
    ax.text(5, 2.7, "Souveraineté technologique · Cameroun", ha="center",
            va="center", fontsize=12, color=RATIS_GOLD, style="italic")
    save(fig, "05_logo_ratis_labs.png", facecolor=RATIS_DARK)


if __name__ == "__main__":
    fig_plan_imprimante(); fig_plan_cnc(); fig_machines_montees()
    fig_fem(); fig_choix_materiau(); fig_carte_contrainte(); fig_logo()
    print("Figures RATISS-ATELIER dans docs/images/")
