"""
Simulation simple de l'atome d'oxygène (modèle de Bohr illustratif)
- Affiche la configuration électronique (1s2 2s2 2p4)
- Optionnel : animation 2D des électrons sur orbites circulaires (requires matplotlib)

Usage:
    python oxygen_sim.py --print        # affiche la configuration et positions initiales
    python oxygen_sim.py --animate      # lance une animation (si matplotlib installé)

Le modèle est purement éducatif (pas une modélisation quantique précise).
"""

from __future__ import annotations
import math
import random
import argparse
import sys

ATOM_NAME = "Oxygène"
Z = 8  # numéro atomique
ELECTRON_CONFIGURATION = [(1, 2), (2, 6)]  # simplified by shell: shell 1 has 2, shell 2 has 6 (2s+4 in 2p)
# More explicit: 1s2, 2s2, 2p4


class Electron:
    def __init__(self, shell: int, angle: float = 0.0, speed: float = 0.05):
        self.shell = shell
        self.angle = angle  # radians
        self.speed = speed  # rad per frame

    def step(self, dt: float = 1.0):
        self.angle = (self.angle + self.speed * dt) % (2 * math.pi)

    def position(self, radius_scale: float = 1.0):
        r = self.shell * radius_scale
        x = r * math.cos(self.angle)
        y = r * math.sin(self.angle)
        return (x, y)


class Atom:
    def __init__(self, Z: int = 8):
        self.Z = Z
        self.electrons: list[Electron] = []
        self._populate_electrons()

    def _populate_electrons(self):
        # Build electrons according to common-shell filling for oxygen
        # Shell 1: 2 electrons; Shell 2: 6 electrons
        self.electrons.clear()
        # shell 1
        for i in range(2):
            angle = 2 * math.pi * i / 2
            speed = 0.12 + (i % 2) * 0.02
            self.electrons.append(Electron(shell=1, angle=angle, speed=speed))
        # shell 2 (6 electrons around)
        for i in range(6):
            angle = 2 * math.pi * i / 6
            speed = 0.07 + (i % 3) * 0.01
            self.electrons.append(Electron(shell=2, angle=angle, speed=speed))

    def step(self, dt: float = 1.0):
        for e in self.electrons:
            e.step(dt)

    def summary(self) -> str:
        lines = []
        lines.append(f"Atome : {ATOM_NAME} (Z={self.Z})")
        lines.append("Configuration (approx.): 1s2 2s2 2p4 -> total 8 électrons")
        lines.append(f"Nombre d'électrons: {len(self.electrons)}")
        shell_counts = {}
        for e in self.electrons:
            shell_counts[e.shell] = shell_counts.get(e.shell, 0) + 1
        for shell in sorted(shell_counts):
            lines.append(f"  couche {shell}: {shell_counts[shell]} électrons")
        return "\n".join(lines)

    def positions(self, radius_scale: float = 1.0):
        return [e.position(radius_scale) for e in self.electrons]


def run_print(atom: Atom):
    print(atom.summary())
    print("Positions initiales (x, y) :")
    for i, (x, y) in enumerate(atom.positions(radius_scale=1.5), start=1):
        print(f"  e{i:02d}: ({x:.3f}, {y:.3f})")


def run_animate(atom: Atom):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
    except Exception as exc:
        print("matplotlib requis pour l'animation. Installez-le via 'pip install matplotlib'", file=sys.stderr)
        raise

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_title(f"Simulation simple : {ATOM_NAME} (Z={atom.Z})")
    ax.axis('off')

    # draw nucleus
    nucleus = plt.Circle((0, 0), 0.3, color='red', alpha=0.8)
    ax.add_artist(nucleus)

    # draw shells (circles)
    shells = [1.5, 3.0]
    for r in shells:
        circle = plt.Circle((0, 0), r, color='gray', fill=False, linestyle='dashed', alpha=0.6)
        ax.add_artist(circle)

    scat = ax.scatter([], [], s=80, c='blue')

    def init():
        scat.set_offsets([])
        return (scat,)

    def update(frame):
        atom.step(dt=1)
        pos = atom.positions(radius_scale=1.5)
        scat.set_offsets(pos)
        return (scat,)

    ani = animation.FuncAnimation(fig, update, frames=600, interval=50, blit=True, init_func=init)
    plt.show()


def main(argv=None):
    parser = argparse.ArgumentParser(description='Simulation simple de l\'atome d\'oxygène (illustratif)')
    parser.add_argument('--animate', action='store_true', help='Afficher une animation (matplotlib requis)')
    parser.add_argument('--print', dest='do_print', action='store_true', help='Afficher la configuration et positions initiales')
    args = parser.parse_args(argv)

    atom = Atom(Z=Z)

    if args.do_print:
        run_print(atom)
        return 0

    if args.animate:
        try:
            run_animate(atom)
        except Exception:
            return 2
        return 0

    # par défaut, print summary
    run_print(atom)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
