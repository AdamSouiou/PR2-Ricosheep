#!/usr/bin/env python3

from sys import setrecursionlimit
from time import time
from copy import deepcopy
from pprint import pprint
from plateau import Plateau
from collections import deque
from multiprocessing import Pool
from os import path
import graphiques
import cfg
import fltk
import solveur
import sauvegarde
import son
import randomizer
import creation_niveaux
import selecteur
import verification

setrecursionlimit(10**6)
DIRECTIONS = {'Up', 'Left', 'Right', 'Down'}


def file_defaite(threads_defaite: deque):
    """
    Traite un résultat de la file FIFO, et
    renvoie ``True`` si la partie devient impossible.

    :param deque threads_defaite: File des threads
    exécutés calculant la viabilité de la partie.
    """
    if threads_defaite:
        if threads_defaite[0].ready():
            chemin, _ = threads_defaite[0].get()
            threads_defaite.popleft()
            if chemin is None:
                return True
    return False


def jeu(plateau: Plateau):
    son.song("Otherside")

    victory_buttons = graphiques.game_over_init("C'est gagné !!", "#008141", "Quitter")
    defeat_buttons = graphiques.game_over_init("C'est perdu :'(", "#A90813", "Reset")
    
    game_over = False
    threads_defaite = deque()
    process_pool = Pool(processes=2)
    
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
                    process_pool.terminate()
                    process_pool.join()
                    return
            
            if file_defaite(threads_defaite) or game_over:
                game_over = True
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
                    son.sound('Sheep')

                    if plateau.deplace_moutons(touche): threads_defaite.append(
                        process_pool.apply_async(
                            solveur.profondeur, (deepcopy(plateau),)
                        )
                    )

                    pprint(threads_defaite)

                if touche == "s":
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
                        print(f"La longueur du chemin est de {len(chemin)},",
                               f"il a fallu {elapsed:.3f}s pour le déterminer.")

                elif touche == "r":
                    game_over = False
                    plateau.reset()
                elif touche == 'u':
                    game_over = False
                    plateau.undo()
                elif touche == 'Escape':
                    threads_defaite.clear()
                    process_pool.terminate()
                    process_pool.join()
                    return
                elif touche == 'p':
                    if cfg.carte_lst == ['custom', 'Random.txt']:
                        selecteur.modif_json('custom', 'Random.txt')
                        creation_niveaux.enregistrement(randomizer.plateau, "Random")
                        sauvegarde.save_write(['custom','Random.txt'], plateau.historique, plateau.troupeau)
                    else:
                        sauvegarde.save_write(cfg.carte_lst, plateau.historique, plateau.troupeau)
                    print("Partie sauvegardée")

            fltk.mise_a_jour()
            dt = time() - dt_start

        except KeyboardInterrupt:
            exit()



if __name__ == "__main__":
    verification.main()
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre,
                    'Ricosheep', icone=path.join('media', 'images', 'icone.ico'))
    son.initialisation()
    from accueil import menu # Evite l'import infini
    menu()
        
