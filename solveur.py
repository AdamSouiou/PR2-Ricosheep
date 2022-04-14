from typing import List, Tuple
from plateau import Plateau
import graphiques
import cfg
import fltk

def profondeur(plateau, direction = None, visite = set(), chemin = []):

    
    if direction != None:
        plateau.deplace_moutons(direction)


    beeeh = tri_copy(plateau.troupeau)


    if plateau.isGagne():
        print("C'est gagné")
        return chemin, visite
    
    if beeeh in visite:
        print("Retour en arrière")
        return chemin, visite
    else:
        if direction is not None:
            chemin.append(direction)
        visite.add(beeeh)
    

    chemin_temp, visite = profondeur(plateau, "Up", visite, chemin)
    if chemin_temp == [None]:
        backup(plateau.troupeau, beeeh)
        return chemin_temp, visite
    chemin = chemin_temp

    chemin_temp, visite = profondeur(plateau, "Right", visite, chemin)
    if chemin_temp == [None]:
        backup(plateau.troupeau, beeeh)
        return chemin_temp, visite
    chemin = chemin_temp

    chemin_temp, visite = profondeur(plateau, "Down", visite, chemin)
    if chemin_temp == [None]:
        backup(plateau.troupeau, beeeh)
        return chemin_temp, visite
    chemin = chemin_temp

    chemin_temp, visite = profondeur(plateau, "Left", visite, chemin)
    if chemin_temp == [None]:
        backup(plateau.troupeau, beeeh)
        return chemin_temp, visite
    chemin = chemin_temp

    return chemin, visite

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
        