from dataclasses import dataclass
from typing import List, Tuple
import graphiques
import cfg
from plateau import Plateau
import fltk


def jeu(plateau: Plateau):

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

            elif tev == "Down":
                pass

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()

fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre)
plateau = Plateau(10, 7)
jeu(plateau)