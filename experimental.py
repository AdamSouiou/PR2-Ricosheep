from typing import List, Tuple, Set
from plateau import Plateau
import fltk
from time import sleep

DIRECTIONS = ("Up", "Right", "Down", "Left")

def precalcul_pos_perdant(
    plateau: Plateau,
    direction = None,
    visite = None) -> Tuple[List[str], Set]:
    """
    Renvoie un dictionnaire des positions de moutons perdantes
    """

    if visite is None:
        visite = {}
        if direction is not None:
            # Au cas où l'on voudrait appeler la fonction
            # avec une direction spécifique
            plateau.deplace_moutons(direction)

    positions_initiales = tri_copy(plateau.troupeau)
    
    if positions_initiales in visite:
        return visite, None
    visite[positions_initiales] = False
    
    if plateau.isGagne():
        visite[positions_initiales] = True
        return visite, True

    for new_dir in DIRECTIONS:
        plateau.deplace_moutons(new_dir)
        visite, gagne = precalcul_pos_perdant(
            plateau, None, visite
        )
        #tested_troupeau = tri_copy(plateau.troupeau)
        if gagne:
            visite[positions_initiales] = True
        """
        if tested_troupeau in visite:
            if visite[tested_troupeau] == True:
                visite[positions_initiales] = True
        """
                
        restore(plateau.troupeau, positions_initiales)

    return visite, False


def tri_copy(troupeau):
    return tuple(sorted(
        [(m.y, m.x) for m in troupeau]
    ))


def restore(troupeau, positions_initiales):
    for i in range(len(troupeau)):
        troupeau[i].x = positions_initiales[i][1]
        troupeau[i].y = positions_initiales[i][0]


if __name__ == '__name__':
    pass