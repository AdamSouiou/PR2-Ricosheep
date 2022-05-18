#!/usr/bin/env python3

from sys import setrecursionlimit
from time import time
from copy import deepcopy
from pprint import pprint
from plateau import Plateau
import graphiques
import cfg
import fltk
import solveur
import sauvegarde
import son


setrecursionlimit(10**6)
DIRECTIONS = {'Up', 'Left', 'Right', 'Down'}


def jeu(plateau: Plateau):
    son.song("Otherside")
    start_deplacement = 0
    dt = 0
    while True:
        try:
            dt_start = time()
            fltk.efface_tout()
            graphiques.background("#3f3e47")
            plateau.draw(start_deplacement, dt)
            
            # if plateau.isGagne():
                # graphiques.victory()
                # print("C'est gagné !")
                # fltk.mise_a_jour()
                # fltk.attend_ev()

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)
            if tev == 'Quitte':
                fltk.ferme_fenetre()
                exit()

            elif tev == "Touche":
                touche = fltk.touche(ev)
                if (touche in DIRECTIONS
                    # Vérifie si un déplacement n'est pas déjà en cours :
                    and plateau.last_direction is None):
                    start_deplacement = time()
                    plateau.deplace_moutons(touche)
                    son.sound('Sheep')
                    # Vérifier ici à ce moment la défaite (attendre la fin du déplacement pour l'annoncer?)

                if touche == "s":
                    plateau.clear_historique()
                    start = time()
                    chemin, _ = solveur.profondeur(deepcopy(plateau))
                    elapsed = time() - start
                    
                    if chemin is None:
                        print("Pas de solutions, chacal!")
                    else:
                        print(chemin)
                        print("Le solveur a bon? :", solveur.test(chemin, plateau))
                        # print(chemin)
                        print(f"La longueur du chemin est de {len(chemin)},",
                              f"il a fallu {elapsed:.3f}s pour le déterminer.")

                elif touche == "r":
                    plateau.reset()
                elif touche == 'u':
                    plateau.undo()
                elif touche == 'Escape':
                    return
                elif touche == 'p':
                    sauvegarde.save_write(cfg.carte_lst, plateau.historique, plateau.troupeau)
                    print("Partie sauvegardée")
                """print('Historique :')
                pprint(plateau.historique)
                print('Troupeau :', plateau.troupeau)
                print()"""

            fltk.mise_a_jour()
            dt = time() - dt_start

        except KeyboardInterrupt:
            exit()


if __name__ == "__main__":
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre,
                      'Ricosheep', icone=None)
    son.initialisation()
    from accueil import menu # Evite l'import infini
    menu()
