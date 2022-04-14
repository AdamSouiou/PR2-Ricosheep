from typing import List, Tuple
from plateau import Plateau
import graphiques
import cfg
import fltk
import copy
import solveur


def jeu(plateau: Plateau):
    reinitialisation = solveur.tri_copy(plateau.troupeau)

    while True:
        try:
            fltk.efface_tout()
            graphiques.background("#3f3e47")

            plateau.draw_grid()
            plateau.draw_moutons()    
        
            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)

            if plateau.isGagne():
                graphiques.victory()
                fltk.mise_a_jour()
                fltk.attend_ev()
                exit()

            if tev == 'Quitte':
                fltk.ferme_fenetre()
                exit()

            elif tev == "Touche":
                direction = fltk.touche(ev)
                plateau.deplace_moutons(direction)

                if direction == "s":
                    chemin = solveur.initProfond(plateau)
                    if chemin == None:
                        print("ptdr t'as perdu chacal")
                    else:
                        print(chemin)

                if direction == "r":
                    solveur.backup(plateau.troupeau, reinitialisation)

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()


if __name__ == "__main__":
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre)
    plateau = Plateau('maps/square/map1.txt')

    jeu(plateau)
