from sys import setrecursionlimit
from time import time
from pprint import pprint
from plateau import Plateau
import graphiques
import cfg
import fltk
import solveur
setrecursionlimit(10**6)

def jeu(plateau: Plateau):
    backup_pos = solveur.tri_copy(plateau.troupeau)

    while True:
        try:
            fltk.efface_tout()
            graphiques.background("#3f3e47")

            plateau.draw_grid()
            plateau.draw_moutons()
            
            if plateau.isGagne():
                # graphiques.victory()
                print("C'est gagné !")
                # fltk.mise_a_jour()
                # fltk.attend_ev()

            ev = fltk.attend_ev()
            tev = fltk.type_ev(ev)
            if tev == 'Quitte':
                fltk.ferme_fenetre()
                exit()

            elif tev == "Touche":
                direction = fltk.touche(ev)
                plateau.deplace_moutons(direction)

                if direction == "s":
                    start = time()
                    chemin, _ = solveur.profondeur(plateau)
                    elapsed = time() - start
                    
                    if chemin == None:
                        print("Pas de solutions, chacal!")
                    else:
                        solveur.test(chemin, plateau)
                        print(chemin)
                        print(f"La longueur du chemin est de {len(chemin)},",
                              f"il a fallu {elapsed:.3f}s pour le déterminer.")

                if direction == "r":
                    solveur.restore(plateau.troupeau, backup_pos)

            fltk.mise_a_jour()
            #fltk.attend_ev()

        except KeyboardInterrupt:
            exit()


if __name__ == "__main__":
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre)
    #plateau = Plateau('maps/big/big1.txt')
    plateau = Plateau('maps/big/huge.txt')
    jeu(plateau)