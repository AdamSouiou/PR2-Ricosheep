from turtle import width
import fltk
import graphiques
import editeur
import cfg
import os
from bouton import Boutons


def menu(plateau):
    boutons = Boutons((10,10))
    boutons.cree_bouton_texte(1, 2, 8, 2, "Voulez-vous enregistrer votre", arrondi = 0.75)
    boutons.cree_bouton_texte(1, 3, 8, 3, "Niveaux ?", arrondi = 0.75)

    boutons.cree_bouton_simple(1, 6, 4, 6, 'Enregistrer', arrondi=0.75)
    boutons.cree_bouton_simple(5, 6, 8, 6, 'Annuler', arrondi=0.75)
    boutons.init()

    while True:
        fltk.efface_tout()
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        graphiques.background("#3f3e47")
        click = boutons.dessiner_boutons(tev)

        if tev == 'Quitte':
            fltk.ferme_fenetre()
            exit()

        if tev == "ClicGauche":
            if click not in {None}:
                if click == "Enregistrer":
                    demande_nom(plateau)
                    return
                    

                elif click == "Annuler":
                        boutons = Boutons((10,10))
                        boutons.cree_bouton_texte(1, 2, 8, 2, "Revenir au menu", arrondi = 0.75)
                        boutons.cree_bouton_texte(1, 3, 8, 3, "principal ?", arrondi = 0.75)

                        boutons.cree_bouton_simple(1, 6, 4, 6, 'Menu', arrondi=0.75)
                        boutons.cree_bouton_simple(5, 6, 8, 6, 'Editeur', arrondi=0.75)
                        boutons.init()
                elif click == "Menu":
                    return
                elif click == "Editeur":
                    editeur.debut()

        fltk.mise_a_jour()

def demande_nom(plateau):
    boutons = Boutons((10,10))
    boutons.cree_bouton_texte(1, 2, 8, 2, "Nom de votre plateau", arrondi = 0.75)
    boutons.cree_bouton_simple(1, 8, 8, 8, "Valider", arrondi = 0.75)

    boutons.init()
    texte = fltk.boite_texte( cfg.largeur_fenetre/6, cfg.hauteur_fenetre/2, "Courier 20", width = 20 )
    while True:
        fltk.efface_tout()
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        graphiques.background("#3f3e47")
        click = boutons.dessiner_boutons(tev)

        if tev == 'Quitte':
            fltk.ferme_fenetre()
            exit()

        if tev == "ClicGauche":
            if click not in {None}:
                fichier = texte.get()
                fichier = fichier.strip()

                if fichier != "":
                    enregistrement(plateau, fichier)
                    fltk.delete_boitetexte(texte)
                    return


        fltk.mise_a_jour()

def enregistrement(plateau, nom):
    file = ""
    with open(os.path.join("maps", "custom", nom+".txt"), 'w') as fichier:
        for ligne in range(len(plateau)):
            temp = ""
            for char in plateau[ligne]:
                if char == None:
                    temp += "_"
                else:
                    temp += str(char)
            file += temp
            if ligne != (len(plateau) - 1):
                file += "\n"

        fichier.write(file)

