from typing import List, Tuple
from plateau import Plateau
import graphiques
import cfg
import fltk

DIRECTIONS = ("Up", "Right", "Down", "Left")

def profondeur(plateau, direction = None, visite = set(), chemin = []):

    plateau.deplace_moutons(direction)
    beeeh = tri_copy(plateau.troupeau)
    
    
    if beeeh in visite:
        print("Retour en arrière")
        return [None], visite
    else:
        chemin.append(direction)
        visite.add(beeeh)
    
    if plateau.isGagne():
        print("C'est gagné")
        return chemin, visite
    
    for dir in DIRECTIONS:
        chemin_temp, visite = profondeur(plateau, dir, visite, chemin)
        if chemin_temp != [None]:
            return chemin_temp, visite

        backup(plateau.troupeau, beeeh)

    return [None], visite


def initProfond(plateau):
    beeeh = tri_copy(plateau.troupeau)

    for dir in DIRECTIONS:

        chemin_temp, _ = profondeur(plateau, dir)
        if chemin_temp != [None]:
            return chemin_temp
        backup(plateau.troupeau, beeeh)

    return None

def tri_copy(troupeau):
    lst = []
    for mouton in troupeau:
        lst.append((mouton.x,mouton.y))
    copy = sorted(lst, key=tri)
    return tuple(copy)

def tri(mouton):
    return mouton[0], mouton[1]

def backup(troupeau, position):
    for i in range(len(troupeau)):
        troupeau[i].x = position[i][0]
        troupeau[i].y = position[i][1]
        