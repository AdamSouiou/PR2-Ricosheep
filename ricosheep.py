#!/usr/bin/env python3
import verification
import cfg
import fltk
import solveur
import sauvegarde
import son
import creation_niveaux
import selecteur
from graphiques import (background, game_over_init,
                        demande_affichage, demande_profondeur)
from functools import partial
from sys import setrecursionlimit
from time import time
from copy import deepcopy
from plateau import Plateau
from bouton import Boutons
from collections import deque
from multiprocessing import Pool
from os import path


setrecursionlimit(10**6)
DIRECTIONS = ('Up', 'Left', 'Right', 'Down')


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


def boutons_jeu_init() -> Boutons:
    """
    Initialisation des boutons de jeu

    :return Boutons: Boutons de jeu.
    """
    boutons = Boutons((20, 23), carre=False)
    boutons.cree_bouton_simple(16, 0, 19, 2, "Reset")
    boutons.cree_bouton_simple(16, 4, 19, 6, "Undo")
    boutons.cree_bouton_simple(16, 8, 19, 10, "Sauvegarde")
    boutons.cree_bouton_simple(16, 12, 19, 14, "Sol. profondeur",
                               unifier_texte=False)
    boutons.cree_bouton_simple(16, 16, 19, 18, "Sol. largeur",
                               unifier_texte=False)
    boutons.cree_bouton_simple(16, 20, 19, 22, "Quitter")
    boutons.init()
    return boutons


def jeu(plateau: Plateau, boutons_jeu):
    son.song("Otherside")
    victory_buttons = game_over_init(
        "C'est gagné !!", "#008141", boutons_jeu.grille)
    defeat_buttons = game_over_init(
        "C'est perdu :'(", "#A90813", boutons_jeu.grille)

    game_over = False
    gagne = False
    threads_defaite = deque()
    process_pool = Pool(processes=2)

    chemin = []
    afficher = False

    start_deplacement = 0
    dt = 0

    while True:
        try:
            dt_start = time()
            fltk.efface_tout()
            background("#3f3e47")
            plateau.draw(start_deplacement, dt)
            boutons_jeu.dessiner_boutons()

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)
            click = boutons_jeu.nom_clic(ev)

            if file_defaite(threads_defaite) or game_over:
                game_over = True
                defeat_buttons.dessiner_boutons(ev)
            elif gagne and not afficher:
                victory_buttons.dessiner_boutons()

            touche = fltk.touche(ev) if tev == "Touche" else None

            if tev == "Quitte":
                fltk.ferme_fenetre()
                exit()

            elif (touche == "Escape"
                  or (tev == "ClicGauche" and click == "Quitter")):
                threads_defaite.clear()
                process_pool.terminate()
                process_pool.join()
                son.song("Wait")
                return

            # Vérifie si un déplacement n'est pas déjà en cours :
            elif (plateau.last_direction is None
                  and (touche in DIRECTIONS or chemin)):
                start_deplacement = time()
                son.sound("Sheep")
                if chemin:
                    touche = chemin.popleft()
                deplacement = plateau.deplace_moutons(touche)

                gagne = False
                if plateau.isGagne():
                    gagne = True

                elif deplacement and not chemin and not game_over:
                    threads_defaite.append(
                        process_pool.apply_async(
                            solveur.iteratif, (deepcopy(plateau), False)
                        )
                    )

            elif tev == "ClicGauche" and not chemin:
                # On bloque le plateau pendant l'affichage de la solution
                son.sound("MenuBleep")

                if click == "Reset":
                    game_over = False
                    gagne = False
                    afficher = False
                    plateau.reset()

                elif click == "Undo":
                    game_over = False
                    gagne = False
                    plateau.undo()

                elif click == "Sauvegarde":
                    if cfg.carte_lst == ["custom", "Random.txt"]:
                        selecteur.modif_json("custom", "Random.txt")
                        plateau_lst = creation_niveaux.plateau_to_ll(plateau)
                        creation_niveaux.enregistrement(
                            plateau_lst, "Random"
                        )
                        sauvegarde.save_write(
                            ["custom", "Random.txt"],
                            plateau.historique, plateau.troupeau
                        )
                    else:
                        sauvegarde.save_write(
                            cfg.carte_lst,
                            plateau.historique, plateau.troupeau
                        )
                    print("Partie sauvegardée")

                elif click in {"Sol. profondeur", "Sol. largeur"}:
                    if click == "Sol. profondeur":
                        solver = demande_profondeur(boutons_jeu.grille)
                    else:
                        solver = partial(solveur.iteratif, largeur=True)
                    start = time()
                    chemin, _ = solver(deepcopy(plateau))
                    elapsed = time() - start

                    if chemin is None:
                        print("Pas de solutions... :( ")
                        game_over = True
                    else:
                        afficher = demande_affichage(boutons_jeu.grille)
                        if afficher:
                            chemin = deque(chemin)
                        print(chemin)
                        print(f"La longueur du chemin est de {len(chemin)}.")
                        print(f"Il a fallu {elapsed:.3f}s pour le déterminer.")
                        if not afficher:
                            chemin = []

            fltk.mise_a_jour()
            dt = time() - dt_start

        except KeyboardInterrupt:
            exit()


if __name__ == "__main__":
    fltk.cree_fenetre(
        cfg.largeur_fenetre, cfg.hauteur_fenetre,
        "Ricosheep", icone=path.join("media", "images", "icone.ico")
    )
    son.initialisation()
    from accueil import menu  # Evite l'import infini
    menu()
    fltk.ferme_fenetre()
