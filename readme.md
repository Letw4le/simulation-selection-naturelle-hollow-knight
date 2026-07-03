# Simulation Hollow Knight

Simulation de vie artificielle réalisée avec **Pygame**, inspirée de l'univers de *Hollow Knight*.
Deux espèces évoluent sur un même écran par sélection génétique : à chaque génération, les individus ayant le mieux survécu transmettent leurs caractéristiques aux suivants, avec quelques mutations aléatoires.

## Prérequis

- Python 3
- [Pygame](https://www.pygame.org/)

```bash
pip install pygame
```

## Lancer la simulation

```bash
python main.py
```

## Principe de la simulation

Trois types d'entités cohabitent sur la carte :

- **Hollow Knights** (`class_hollow_knights.py`) — l'espèce principale. Chaque individu possède une vie, une vitesse, un comportement et une taille, et doit survivre en évitant les virus jaunes tout en mangeant des virus bleus pour ne pas mourir de faim.
- **Virus bleus** (`class_virus_bleu.py`) — servent de nourriture aux Hollow Knights. Ils peuvent adopter un comportement normal ou fuyant, et évoluent également par génération.
- **Virus jaunes** (`class_virus_jaune.py`) — l'infection. Ils se déplacent aléatoirement en rebondissant sur les bords de l'écran et retirent de la vie à tout individu qu'ils touchent. Leur vitesse augmente chaque minute.

### Comportements des Hollow Knights

- `déviant` — se déplace de façon totalement aléatoire.
- `gourmand` — cherche activement le virus bleu le plus proche pour se nourrir (10 repas = 1 vie supplémentaire).
- `peureux` — fuit le virus jaune le plus proche.

### Cycle de génération

Une génération se termine quand tous les Hollow Knights sont morts ( pour les virus bleu c'est quand il en reste plus qu'un). Les caractéristiques (vie, vitesse, comportement, taille) de l'individu ayant vécu le plus longtemps sont alors mélangées avec celles des autres pour créer la génération suivante, avec une mutation aléatoire à chaque individu.

## Contrôles

- **Start / Restart** — démarre une nouvelle simulation.
- **Continue** — reprend la dernière sauvegarde (`save.txt`), si elle existe.
- **Quit** — quitte le jeu.
- **Bouton x2** (en haut à droite) — accélère la vitesse de la simulation.
- **Bouton save** (en haut à droite) — sauvegarde l'état actuel de la simulation dans `save.txt`.

## Structure du projet

| Fichier                      | Rôle                                                           |
|------------------------------|----------------------------------------------------------------|
| `main.py`                    | Boucle principale, menu, gestion des générations et collisions |
| `class_hollow_knights.py`    | Classe de l'espèce principale                                  |
| `class_virus_bleu.py`        | Classe des virus bleus (nourriture)                            |
| `class_virus_jaune.py`       | Classe des virus jaunes (infection)                            |
| `game_time.py`               | Horloge du jeu (thread séparé)                                 |
| `class_btn_img.py`           | Boutons image (save, x2)                                       |
| `menu.py`                    | Boutons du menu principal                                      |
| `save.txt`                   | Fichier de sauvegarde généré par la simulation                 |
| `img_hollow_knight/`         | Sprites des différents Hollow Knights                          |
