from typing import List, Tuple, Set
from plateau import Plateau
import fltk
from time import sleep

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
        plateau.deplace_moutons(direction)

    positions_initiales = tri_copy(plateau.troupeau)
    
    if positions_initiales in visite:
        return None, visite
    
    visite.add(positions_initiales)

    if plateau.isGagne():
        return [], visite
    
    for new_dir in DIRECTIONS:
        plateau.deplace_moutons(new_dir)
        chemin.append(new_dir)
        chemin_temp, visite = profondeur(
            plateau, None, visite, chemin
        )
        if chemin_temp is not None:
            return chemin, visite
        chemin.pop()
        restore(plateau.troupeau, positions_initiales)

    return None, visite


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

def test(chemin: List[str], plateau: Plateau, anim=0):
    for mouv in chemin:
        plateau.deplace_moutons(mouv)
        if anim: anim_brute(plateau, anim)
    return plateau.isGagne()

if __name__ == '__name__':
    pass