from typing import List, Tuple, Set
from plateau import Plateau
import fltk
from time import sleep
import collections

DIRECTIONS = ("Up", "Right", "Down", "Left")

def profondeur(plateau,
               direction = None,
               visite = None,
               chemin = None) -> Tuple[List[str], Set]:

    if visite is None and chemin is None:
        visite = set()
        chemin = []
        if direction is not None:
            # Au cas où l'on voudrait appeler la fonction
            # avec une direction spécifique
            chemin.append(direction)
            plateau.deplace_moutons(direction, solveur=True)

    positions_initiales = tri_copy(plateau.troupeau)
    
    if positions_initiales in visite:
        return None, visite
    
    visite.add(positions_initiales)

    if plateau.isGagne():
        return [], visite
    
    for new_dir in DIRECTIONS:
        plateau.deplace_moutons(new_dir, solveur=True)
        chemin.append(new_dir)
        chemin_temp, visite = profondeur(
            plateau, None, visite, chemin
        )
        if chemin_temp is not None:
            return chemin, visite
        chemin.pop()
        restore(plateau.troupeau, positions_initiales)

    return None, visite


def largeur(plateau) -> List[str]:

    directions = DIRECTIONS
    visite = set()
    parcours = collections.deque()
    parcours.append((tri_copy(plateau.troupeau), []))
    
    while parcours:
        positions, chemin = parcours.popleft()
        restore(plateau.troupeau, positions)

        if plateau.isGagne():
            return chemin

        if positions in visite:
            continue

        visite.add(positions)
        
        if chemin:
            if   chemin[-1] in ("Up", "Down"): directions = ("Left", "Right")
            elif chemin[-1] in ("Right", "Left"): directions = ("Up", "Down")

        for direction in directions:
            plateau.deplace_moutons(direction, solveur=True)
            parcours.append((tri_copy(plateau.troupeau), chemin + [direction]))
            restore(plateau.troupeau, positions)
    
    return None


def tri_copy(troupeau):
    return tuple(sorted(
        [(m.y, m.x) for m in troupeau]
    ))


def restore(troupeau, positions_initiales):
    for i in range(len(troupeau)):
        troupeau[i].x = positions_initiales[i][1]
        troupeau[i].y = positions_initiales[i][0]

""" 
def tri_copy(troupeau):
    return tuple(sorted(troupeau))

def restore(troupeau, positions_initiales):
    for i in range(len(troupeau)):
        troupeau[i].x = positions_initiales[i].x
        troupeau[i].y = positions_initiales[i].y
"""

def anim_brute(plateau: Plateau, pause: int):
        
    fltk.efface_tout()
    plateau.draw()
    fltk.mise_a_jour()
    sleep(pause)

def test(chemin: List[str], plateau: Plateau, unittest=False):
    for mouv in chemin:
        plateau.deplace_moutons(mouv, solveur=True)

    if not unittest: plateau.reposition_moutons()
    return plateau.isGagne()

if __name__ == '__name__':
    pass