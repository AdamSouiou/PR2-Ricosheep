from plateau import Plateau
import random
import editeur
import cfg
import os

#ATTENTION! Au dela d'un plateau 7x7, l'application crash sans donner d'erreur.
#Crash générer lors d'un random entre 5x5 et 8x8

def generation100():
    global plateau
    test = False
    while not test:
        nb_colonnes = random.randint(5,7)
        nb_lignes = random.randint(5,7)

        plateau = []
        for _ in range(nb_lignes):
            ligne = []
            for _ in range(nb_colonnes):
                case = random.randint(1,12)
                if case <= 5:
                    ligne.append(editeur.ETAT[0])
                elif case <= 10:
                    ligne.append(editeur.ETAT[1])
                elif case == 11:
                    ligne.append(editeur.ETAT[2])
                elif case == 12:
                    ligne.append(editeur.ETAT[3])
            plateau.append(ligne)
        test, chemin = editeur.test(plateau, False)
        if len(chemin) <= 10:
            test = False
    print(nb_colonnes,nb_lignes)
    cfg.carte_lst = ['custom', 'Random.txt']
    return plateau
        


