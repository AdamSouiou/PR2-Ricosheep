from plateau import Plateau
from bouton import Boutons
import son
import graphiques 
import fltk
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
        nb_colonnes = random.randint(4,9)
        nb_lignes = random.randint(4,9)

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
        #print(len(chemin), chemin)
        if len(chemin) <= 3:
            test = False
    #print(nb_colonnes,nb_lignes)
    cfg.carte_lst = ['custom', 'Random.txt']
    return plateau

def aleatoirecontrole(liste):
    global plateau
    test= False

    while not test:
        plateau = []
        lignes = liste[0]
        colonnes = liste[1]
        moutons = liste[2]
        herbes = liste[3]
        buisson = 0
        for _ in range(lignes):
            ligne=[]
            for _ in range(colonnes):
                if (lignes*colonnes) > (moutons+herbes+buisson):
                    etat = random.getrandbits(1)
                    ligne.append(editeur.ETAT[etat])
                    if etat == 1:
                        buisson += 1
                else:
                    ligne.append(editeur.ETAT[0])

            plateau.append(ligne)
        print(plateau)
        while moutons != 0:
            casex = random.randint(0, lignes-1)
            casey = random.randint(0, colonnes-1)
            
            if plateau[casex][casey] == "_":
                plateau[casex][casey] = editeur.ETAT[3]
                moutons -= 1
        print(plateau)
        
        while herbes != 0:
            casex = random.randint(0, lignes-1)
            casey = random.randint(0, colonnes-1)
            if plateau[casex][casey] == "_":
                plateau[casex][casey] = editeur.ETAT[2]
                herbes -= 1
        print(plateau, "\n")

        test, chemin = editeur.test(plateau, False)
        print(len(chemin), chemin)
        if len(chemin) != liste[4]:
            test = False
        cfg.carte_lst = ['custom', 'Random.txt']
    return plateau
            


def menu_control():
    boutons = Boutons((10,10))
    boutons.cree_bouton_texte(1, 2, 5, 2, "Nombre de lignes :", arrondi=0.75)
    boutons.entree_texte(7, 2, 8, 2, "lignes")

    boutons.cree_bouton_texte(1, 3, 5, 3, "Nombre de colonnes :", arrondi=0.75)
    boutons.entree_texte(7, 3, 8, 3, "colonnes")

    boutons.cree_bouton_texte(1, 4, 5, 4, "Nombre de moutons :", arrondi=0.75)
    boutons.entree_texte(7, 4, 8, 4, "moutons")

    boutons.cree_bouton_texte(1, 5, 5, 5, "Nombre de touffes :", arrondi=0.75)
    boutons.entree_texte(7, 5, 8, 5, "herbes")

    boutons.cree_bouton_texte(1, 6, 5, 6, "Nombre de coups :", unifier_texte=False, arrondi=0.75)
    boutons.entree_texte(7, 6, 8, 6, "difficulte")

    boutons.cree_bouton_simple(2, 8, 7, 8, "Valider", arrondi = 1)
    
    entiers_positifs = "Veuillez insérer que des entiers positifs !"
    boutons.cree_bouton_texte(1, 9, 8, 9, entiers_positifs,
                              invisible=True, couleur_texte='red')

    règle_de_jeuM = "Il vous faut au moins autant de moutons que d'herbes !"
    boutons.cree_bouton_texte(1, 9, 8, 9, règle_de_jeuM,
                              invisible=True, couleur_texte='red', unifier_texte=False)
    
    règle_de_jeuT = "Le plateau doit pouvoir contenir tous les éléments!"
    boutons.cree_bouton_texte(1, 9, 8, 9, règle_de_jeuT,
                              invisible=True, couleur_texte='red', unifier_texte=False)

    boutons.init()
    ev = None

    while True:
        fltk.efface_tout()
        graphiques.background("#3f3e47")
        boutons.dessiner_boutons(ev)
        
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        click = boutons.nom_clic(ev)

        if tev == 'Quitte':
            boutons.destroy_entree_textes()
            graphiques.close()
        if tev == "Touche":
            if fltk.touche(ev) == "Escape":
                boutons.destroy_entree_textes()
                return

        if tev == "ClicGauche":
            if click not in {None}:
                son.sound('MenuAccept')
                nb_lignes = boutons.entrees_texte['lignes'].get()
                nb_colonnes = boutons.entrees_texte['colonnes'].get()
                nb_moutons = boutons.entrees_texte['moutons'].get()
                nb_herbes = boutons.entrees_texte['herbes'].get()
                nb_coups = boutons.entrees_texte['difficulte'].get()

                liste = [nb_lignes, nb_colonnes, nb_moutons, nb_herbes, nb_coups]

                for i in range(len(liste)):
                    if liste[i].isdigit():
                        liste[i] = int(liste[i])
                        changement = True
                    
                    else:
                        changement = False
                        break


                if changement:
                    
                    if liste[0]> 0 and liste[1]> 0 and liste[2]> 0 and liste[3] >0 and liste[4] >0:
                        boutons.boutons[entiers_positifs].invisible = True

                        if liste[2] < liste[3]:
                            boutons.boutons[règle_de_jeuM].invisible = False
                            boutons.boutons[règle_de_jeuT].invisible = True

                        elif (liste[0] * liste[1]) <= (liste[2] + liste[3]):
                            boutons.boutons[règle_de_jeuT].invisible = False
                            boutons.boutons[règle_de_jeuM].invisible = True
  
                        else:
                            boutons.destroy_entree_textes()
                            return aleatoirecontrole(liste)   

                    else:
                        boutons.boutons[entiers_positifs].invisible = False
                        boutons.boutons[règle_de_jeuT].invisible = True
                        boutons.boutons[règle_de_jeuM].invisible = True

        fltk.mise_a_jour()
        


