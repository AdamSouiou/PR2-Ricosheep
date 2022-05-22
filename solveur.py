"""
Projet 2 : Ricosheep

Amal ABDALLAH
Nicolas SEBAN
Adam SOUIOU
"""

from typing import List, Tuple, Set, Optional
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from plateau import Plateau
from collections import deque
from functools import partial
from mouton import Mouton


DIRECTIONS = ("Up", "Right", "Down", "Left")
DIRECTIONS_UP_DOWN = ('Up', 'Down')
DIRECTIONS_LEFT_RIGHT = ('Left', 'Right')


def profondeur(plateau: "Plateau",
               direction: Optional[str] = None,
               visite: Optional[Set[tuple]] = None,
               chemin: Optional[List[str]] = None) -> Tuple[List[str], Set]:
    """
    Fonction récursive qui retourne le chemin vers la solution et les cases visités pour un plateau donné. 

    :param Plateau plateau: Plateau de jeu
    :param str direction: Direction jouée lors de la fonction précédente
    :param Set[tuple] visite: Set de tous les emplacements de moutons déjà visités
    :param list[str] chemin: Chemin du troupeau jusqu'à présent.
    :return Tuple[List[str], Set]: Tuple du chemin et des emplacements visités
    """
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


def iteratif(plateau: "Plateau", largeur: Optional[bool]=False) -> List[str]:
    """
    Fonction itérative qui retourne le chemin vers la solution d'un plateau donné.
    Dans le cas ou "largeur" est True, alors c'est la solution minimale qui sera donné.

    :param Plateau plateau: Plateau de jeu
    :param bool largeur: Si la fonction passe en mode solution minimale.
    :return list: Liste du chemin de la solution.
    """
    directions = DIRECTIONS
    visite = set()
    parcours = deque()
    parcours.append((tri_copy(plateau.troupeau), []))
    popping = (partial(parcours.popleft) if largeur
              else partial(parcours.pop))
    
    while parcours:
        positions, chemin = popping()
        restore(plateau.troupeau, positions)

        if plateau.isGagne():
            return chemin, visite

        if positions in visite:
            continue

        visite.add(positions)
        
        if chemin:
            if   chemin[-1] in DIRECTIONS_UP_DOWN: directions = DIRECTIONS_LEFT_RIGHT
            elif chemin[-1] in DIRECTIONS_LEFT_RIGHT: directions = DIRECTIONS_UP_DOWN

        for direction in directions:
            plateau.deplace_moutons(direction, solveur=True)
            parcours.append((tri_copy(plateau.troupeau), chemin + [direction]))
            restore(plateau.troupeau, positions)

    return None, visite


def tri_copy(troupeau: List[Mouton]) -> Tuple[Tuple[int, int]]:
    """
    Tri la liste de moutons et selon leur coordonnés y et x et renvoie un tuple avec uniquement leur coordonnée
    
    :param List[Mouton] troupeau: Liste des moutons
    :return Tuple[Tuple[int, int]]: Tuple de coordonnées de chaque mouton du troupeau trié.
    """
    return tuple(sorted(
        [(m.y, m.x) for m in troupeau]
    ))


def restore(troupeau: List[Mouton], positions_initiales: Tuple[Tuple[int, int]]) -> None:
    """
    Remplace les coordonnées des moutons selon une copie d'une position précédente.

    :param List[Mouton] troupeau: Liste des moutons
    :param Tuple[Tuple[int, int]] positions_initiales: Tuple de coordonnées précédente de chaque mouton du troupeau.
    """
    for i in range(len(troupeau)):
        troupeau[i].x = positions_initiales[i][1]
        troupeau[i].y = positions_initiales[i][0]

if __name__ == '__name__':
    pass