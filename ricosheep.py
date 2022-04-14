from typing import List, Tuple
from plateau import Plateau
import graphiques
import cfg
import fltk
import copy
import solveur


def jeu(plateau: Plateau):
    while True:
        try:
            fltk.efface_tout()
            graphiques.background("#3f3e47")

            plateau.draw_grid()
            plateau.draw_moutons()    
                    
            ev = fltk.donne_ev() # fltk.attend_ev()
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
                    print(solveur.profondeur(plateau))

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()


if __name__ == "__main__":
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre)
    plateau = Plateau('maps/big/big1.txt')

    jeu(plateau)
