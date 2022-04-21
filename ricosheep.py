from sys import setrecursionlimit
from time import time
from pprint import pprint
from plateau import Plateau
from menu import menu
import graphiques
import cfg
import fltk
import solveur
import experimental

setrecursionlimit(10**6)

def jeu(plateau: Plateau):
    pos_initiale = solveur.tri_copy(plateau.troupeau)
    if cfg.precalcul_perdant: pos_perdantes, _ = experimental.precalcul_pos_perdant(plateau)

    while True:
        try:
            fltk.efface_tout()
            graphiques.background("#3f3e47")

            plateau.draw()
            
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
                touche = fltk.touche(ev)
                plateau.deplace_moutons(touche)
                if cfg.precalcul_perdant:
                    t = solveur.tri_copy(plateau.troupeau)
                    print(f"{plateau.troupeau}")
                    print(f"Valeur calculée par pos_perdant pour le troupeau :")
                    if t in pos_perdantes:
                        print(f"{pos_perdantes[t]}")
                    else:
                        print("Ce cas n'est pas présent dans les positions calculées")
                    print()

                if touche == "s":
                    start = time()
                    pos_tmp = solveur.tri_copy(plateau.troupeau)
                    chemin, _ = solveur.profondeur(plateau)
                    elapsed = time() - start
                    
                    if chemin == None:
                        print("Pas de solutions, chacal!")
                    else:
                        solveur.restore(plateau.troupeau, pos_tmp)
                        print(chemin)
                        print("Le solveur a bon? :", solveur.test(chemin, plateau, 0))
                        # print(chemin)
                        print(f"La longueur du chemin est de {len(chemin)},",
                              f"il a fallu {elapsed:.3f}s pour le déterminer.")

                elif touche == "r":
                    solveur.restore(plateau.troupeau, pos_initiale)
                elif touche == 'Escape':
                    return

            fltk.mise_a_jour()
            #fltk.attend_ev()

        except KeyboardInterrupt:
            exit()


if __name__ == "__main__":
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre)

    while True:
        choix = menu()
        if choix == 'Jouer':
            plateau = Plateau('maps/tests/losable.txt')
            jeu(plateau)

