#!/usr/bin/env python3

from sys import setrecursionlimit
from time import time
from copy import deepcopy
from pprint import pprint
from plateau import Plateau
import concurrent.futures
import graphiques
import cfg
import fltk
import solveur
import sauvegarde
import son
import randomizer
import creation_niveaux
import selecteur
import os
import verification

setrecursionlimit(10**6)
DIRECTIONS = {'Up', 'Left', 'Right', 'Down'}

def jeu(plateau: Plateau):
    son.song("Otherside")

    victory_buttons = graphiques.game_over_init("C'est gagné !!", "#008141", "Quitter")
    defeat_buttons = graphiques.game_over_init("C'est perdu :'(", "#A90813", "Reset")
    game_over = False

    start_deplacement = 0
    dt = 0
    while True:
        try:
            dt_start = time()
            fltk.efface_tout()
            graphiques.background("#3f3e47")
            plateau.draw(start_deplacement, dt)

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)

            if plateau.isGagne():
                
                victory_buttons.dessiner_boutons(ev)
                click = victory_buttons.nom_clic(ev)
                if click == "Quitter" and tev == "ClicGauche":
                    return

            elif game_over == True:
                defeat_buttons.dessiner_boutons(ev)
                click = defeat_buttons.nom_clic(ev)
                if click == "Reset" and tev == "ClicGauche":
                    plateau.reset()
                    game_over = False

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

                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(solveur.profondeur, deepcopy(plateau))
                    historique = plateau.historique

                    son.sound('Sheep')
                    chemin, _ = future.result()
                    plateau.historique = historique

                    if chemin is None:
                        print(game_over)
                        game_over = True
                    else:
                        game_over = False


                if touche == "s":
                    if len(plateau.historique) <= 1:
                        print("test")
                        start = time()
                        chemin, _ = solveur.profondeur(deepcopy(plateau))
                        elapsed = time() - start
                    
                    if chemin is None:
                        print("Pas de solutions, chacal!")
                        game_over = True
                    else:
                        print(chemin)
                        print("Le solveur a bon? :", solveur.test(chemin, plateau))
                        # print(chemin)
                        print(f"La longueur du chemin est de {len(chemin)},")
                            #   f"il a fallu {elapsed:.3f}s pour le déterminer.")

                elif touche == "r":
                    game_over = False
                    plateau.reset()
                elif touche == 'u':
                    game_over = False
                    plateau.undo()
                elif touche == 'Escape':
                    return
                elif touche == 'p':
                    if cfg.carte_lst == ['custom', 'Random.txt']:
                        selecteur.modif_json('custom', 'Random.txt')
                        creation_niveaux.enregistrement(randomizer.plateau, "Random")
                        sauvegarde.save_write(['custom','Random.txt'], plateau.historique, plateau.troupeau)
                    else:
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
    verification.main()
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre,
                    'Ricosheep', icone= os.path.join("media", "images", "Illustration.png"))
    son.initialisation()
    from accueil import menu # Evite l'import infini
    menu()
        
