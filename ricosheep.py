from typing import List, Tuple
from plateau import Plateau
import graphiques
import cfg
import fltk
import copy


def jeu(plateau: Plateau):
    while True:
        try:
            fltk.efface_tout()
            graphiques.background("#3f3e47")
            plateau.draw_moutons()
            plateau.draw_grid()
            
            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)

            if tev == 'Quitte':
                fltk.ferme_fenetre()
                exit()

            elif tev == "Touche":
                direction = fltk.touche(ev)
                plateau.deplace_moutons(direction)

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()


if __name__ == "__main__":
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre)
    plateau = Plateau(
        raw_plateau=[
            ['G', None, 'B', 'None'],
            [None, None, None, None],
            ['G', None, 'B', 'None'],
            [None, None, None, None],
            [None, None, None, None]
        ],
        raw_moutons=((0, 1), (3, 1))
    )
    l = []
    for i in range(10):
        l.append(copy.copy(plateau))
    jeu(plateau)
