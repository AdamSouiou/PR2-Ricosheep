from dataclasses import dataclass
from typing import List, Tuple
from mouton import Mouton
from plateau import Plateau
import graphiques
import cfg
import fltk


def jeu(plateau: Plateau):
    sheep = Mouton(5,7)
    while True:
        try:
            fltk.efface_tout()
            graphiques.background("#3f3e47")
            plateau.draw()
            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)

            if tev == 'Quitte':
                fltk.ferme_fenetre()
                exit()

            elif tev == "Touche":
                direction = fltk.touche(ev)
                sheep.deplace_mouton(direction, Plateau)


            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()


if __name__ == "__main__":
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre)
    plateau = Plateau(10, 7)
    jeu(plateau)