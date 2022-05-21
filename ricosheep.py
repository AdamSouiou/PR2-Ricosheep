#!/usr/bin/env python3
import verification
import graphiques
import cfg
import fltk
import solveur
import sauvegarde
import son
import randomizer
import creation_niveaux
import selecteur
from sys import setrecursionlimit
from time import time
from copy import deepcopy
from pprint import pprint
from plateau import Plateau
from bouton import Boutons
from collections import deque
from multiprocessing import Pool
from os import path


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

def boutons_jeu_init():
    boutons = Boutons((20,23), carre=False)
    boutons.cree_bouton_simple(16, 0, 19, 2, "Reset")
    boutons.cree_bouton_simple(16, 4, 19, 6, "Undo")
    boutons.cree_bouton_simple(16, 8, 19, 10, "Sauvegarde")
    boutons.cree_bouton_simple(16, 12, 19, 14, "Sol. profondeur", unifier_texte=False)
    boutons.cree_bouton_simple(16, 16, 19, 18, "Sol. largeur", unifier_texte=False)
    boutons.cree_bouton_simple(16, 20, 19, 22, "Quitter")
    boutons.init()
    return boutons


def jeu(plateau: Plateau, boutons_jeu):
    son.song('Otherside')
    victory_buttons = graphiques.game_over_init(
        "C'est gagné !!", "#008141", boutons_jeu.grille)
    defeat_buttons = graphiques.game_over_init(
        "C'est perdu :'(", "#A90813", boutons_jeu.grille)
    
    game_over = False
    threads_defaite = deque()
    process_pool = Pool(processes=2)
    
    chemin = []
    
    start_deplacement = 0
    dt = 0

    while True:
        try:
            dt_start = time()
            fltk.efface_tout()
            graphiques.background("#3f3e47")
            plateau.draw(start_deplacement, dt)
            boutons_jeu.dessiner_boutons()

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)
            click = boutons_jeu.nom_clic(ev)

            if plateau.isGagne():
                victory_buttons.dessiner_boutons()
            
            elif file_defaite(threads_defaite):
                game_over = True

            elif game_over:
                defeat_buttons.dessiner_boutons(ev)

            touche = fltk.touche(ev) if tev == 'Touche' else None

            if tev == 'Quitte':
                fltk.ferme_fenetre()
                exit()

            elif (touche == 'Escape'
                 or (tev == 'ClicGauche' and click == "Quitter")):
                threads_defaite.clear()
                process_pool.terminate()
                process_pool.join()
                son.song("Wait")
                return

            # Vérifie si un déplacement n'est pas déjà en cours :
            elif (plateau.last_direction is None
                and (touche in DIRECTIONS or chemin)): # Si le chemin n'est pas vide
                start_deplacement = time()
                son.sound('Sheep')
                if chemin:
                    touche = chemin.pop(0)
                deplacement = plateau.deplace_moutons(touche)

                if deplacement and not chemin: threads_defaite.append(
                    process_pool.apply_async(
                        solveur.profondeur, (deepcopy(plateau),)
                    )
                )

            elif tev == "ClicGauche" and not chemin:
                # On bloque le plateau pendant l'affichage de la solution
                son.sound('MenuBleep')

                if click == "Reset":
                    game_over = False
                    plateau.reset()

                elif click == "Undo":
                    game_over = False
                    plateau.undo()

                elif click == "Sauvegarde":
                    if cfg.carte_lst == ['custom', 'Random.txt']:
                        selecteur.modif_json('custom', 'Random.txt')
                        creation_niveaux.enregistrement(
                            randomizer.plateau, "Random"
                        )
                        sauvegarde.save_write(
                            ['custom','Random.txt'],
                            plateau.historique, plateau.troupeau
                        )
                    else:
                        sauvegarde.save_write(
                            cfg.carte_lst,
                            plateau.historique, plateau.troupeau
                        )
                    print("Partie sauvegardée")

                elif click in {"Sol. profondeur", "Sol. largeur"}:
                    solver = (solveur.largeur if click == "Sol. largeur"
                             else solveur.profondeur)
                    start = time()
                    chemin = solver(deepcopy(plateau))
                    elapsed = time() - start

                    if chemin is None:
                        print("Pas de solutions, chacal!")
                        game_over = True
                    else:
                        print(chemin)
                        print(f"La longueur du chemin est de {len(chemin)},")
                        print(f"Il a fallu {elapsed:.3f}s pour le déterminer.")

            fltk.mise_a_jour()
            dt = time() - dt_start

        except KeyboardInterrupt:
            exit()


if __name__ == "__main__":
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre,
                    'Ricosheep', icone=path.join('media', 'images', 'icone.ico'))
    son.initialisation()
    from accueil import menu # Evite l'import infini
    menu()
    fltk.ferme_fenetre()
