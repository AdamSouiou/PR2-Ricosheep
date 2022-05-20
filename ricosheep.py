#!/usr/bin/env python3

from sys import setrecursionlimit
from time import time
from copy import deepcopy
from pprint import pprint
from plateau import Plateau
from bouton import Boutons
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

def boutons_jeu_init():
    boutons = Boutons((20,23), carre=False)
    boutons.cree_bouton_simple(16, 0, 19, 2, "Reset", unifier_texte=False)
    boutons.cree_bouton_simple(16, 4, 19, 6, "Undo", unifier_texte=False)
    boutons.cree_bouton_simple(16, 8, 19, 10, "Sauvegarde", unifier_texte=False)
    boutons.cree_bouton_simple(16, 12, 19, 14, "Solveur profondeur", unifier_texte = False)
    boutons.cree_bouton_simple(16, 16, 19, 18, "Solveur largeur", unifier_texte=False)
    boutons.cree_bouton_simple(16, 20, 19, 22, "Quitter", unifier_texte= False)
    boutons.init()
    return boutons


def jeu(plateau: Plateau, boutons_jeu):
    son.song('Otherside')


    victory_buttons = graphiques.game_over_init("C'est gagné !!", "#008141", boutons_jeu.grille)
    defeat_buttons = graphiques.game_over_init("C'est perdu :'(", "#A90813", boutons_jeu.grille)
    
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
            boutons_jeu.dessiner_boutons()

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)
            click = boutons_jeu.nom_clic(ev)

            if plateau.isGagne():
                victory_buttons.dessiner_boutons()
                if click == "Quitter" and tev == "ClicGauche":
                    process_pool.terminate()
                    process_pool.join()
                    son.song("Wait")
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

            elif tev == "ClicGauche":
                if click is not None:
                    son.sound('MenuBleep')
                    if click == "Reset":
                        game_over = False
                        plateau.reset()

                    elif click =="Undo":
                        game_over = False
                        plateau.undo()

                    elif click =="Sauvegarde":
                        if cfg.carte_lst == ['custom', 'Random.txt']:
                            selecteur.modif_json('custom', 'Random.txt')
                            creation_niveaux.enregistrement(randomizer.plateau, "Random")
                            sauvegarde.save_write(['custom','Random.txt'], plateau.historique, plateau.troupeau)
                        else:
                            sauvegarde.save_write(cfg.carte_lst, plateau.historique, plateau.troupeau)
                        print("Partie sauvegardée")

                    elif click =="Solveur profondeur":
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
                            #print(f"il a fallu {elapsed:.3f}s pour le déterminer.")

                    elif click =="Solveur largeur":
                        pass

                    elif click =="Quitter":
                        threads_defaite.clear()
                        process_pool.terminate()
                        process_pool.join()
                        son.song("Wait")
                        return


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

                if touche == 'Escape':
                    threads_defaite.clear()
                    process_pool.terminate()
                    process_pool.join()
                    son.song("Wait")
                    return


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
    fltk.ferme_fenetre()
