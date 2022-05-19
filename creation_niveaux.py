import fltk
import graphiques
import editeur
import cfg
import os
import son
from bouton import Boutons


def menu(plateau):
    boutons = Boutons((10,10))
    boutons.cree_bouton_texte(1, 2, 8, 2, "Voulez-vous enregistrer")
    boutons.cree_bouton_texte(1, 3, 8, 3, "votre niveau ?")

    boutons.cree_bouton_simple(1, 6, 4, 6, 'Enregistrer', arrondi=0.75)
    boutons.cree_bouton_simple(5, 6, 8, 6, 'Annuler', arrondi=0.75)
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
            fltk.ferme_fenetre()
            exit()

        if tev == "ClicGauche":
            if click not in {None}:
                if click == "Enregistrer":
                    son.sound('MenuOk')
                    demande_nom(plateau)
                    return
                    

                elif click == "Annuler":
                    son.sound('Menubeep')
                    boutons = Boutons((10,10))
                    boutons.cree_bouton_texte(1, 2, 8, 2, "Revenir au menu", arrondi = 0.75)
                    boutons.cree_bouton_texte(1, 3, 8, 3, "principal ?", arrondi = 0.75)

                    boutons.cree_bouton_simple(1, 6, 4, 6, 'Menu', arrondi=0.75)
                    boutons.cree_bouton_simple(5, 6, 8, 6, 'Editeur', arrondi=0.75)
                    boutons.init()
                elif click == "Menu":
                    son.sound('MenuOk')
                    return
                elif click == "Editeur":
                    son.sound('Menubeep')
                    editeur.debut()

        fltk.mise_a_jour()

def demande_nom(plateau):
    boutons = Boutons((10,10))
    boutons.cree_bouton_texte(1, 2, 8, 2, "Nom de votre plateau", arrondi = 0.75)
    boutons.cree_bouton_simple(1, 8, 8, 8, "Valider", arrondi = 0.75)
    boutons.entree_texte(1, 4, 8, 4, 'filename')

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
            fltk.ferme_fenetre()
            exit()

        if tev == "ClicGauche":
            if click is not None:
                son.sound('MenuOk')
                fichier = boutons.entrees_texte['filename'].get()
                fichier = fichier.strip()

                if fichier != "":
                    enregistrement(plateau, fichier)
                    return


        fltk.mise_a_jour()

def enregistrement(plateau, nom):
    file = ""
    with open(os.path.join("maps", "custom", nom+".txt"), 'w') as fichier:
        for ligne in plateau:
            file += ''.join(ligne)
            if ligne != (len(plateau) - 1):
                file += "\n"

        fichier.write(file)
