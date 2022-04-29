import fltk
from bouton import Boutons
import graphiques
import cfg

from tkinter import Entry

ETAT = [None, "Buisson", "Touffe", "Mouton"]


def init_boutons(Echec = False):
    boutons = Boutons((10,10))
    boutons.cree_bouton_texte(1, 2, 8, 2, "Nombre de lignes", arrondi=0.75)
    boutons.cree_bouton_texte(1, 4, 8, 4, "Nombre de colonnes", arrondi=0.75)
    boutons.cree_bouton_simple(1, 6, 8, 6, "Valider", arrondi = 1)

    if Echec:
        boutons.cree_bouton_texte(1, 1, 8, 1, "Veuillez mettre que des entiers positifs.", unifier_texte= False)

    boutons.init()
    return boutons

def init_boutons_grille(nb_lignes, nb_colonnes):
    Liste = []
    boutons = Boutons((nb_lignes, nb_colonnes))
    for colonne in range(nb_colonnes):
        temp = []
        for ligne in range(nb_lignes):
            temp.append([None, 0])
            boutons.cree_bouton_invisible(ligne, colonne, ligne, colonne, f"{colonne} {ligne}")
        Liste.append(temp)
    return boutons, Liste

def change_case(plateau, coord):
    print( plateau[coord[0]][coord[1]])
    num = (plateau[coord[0]][coord[1]][1] + 1 ) % 4
    plateau[coord[0]][coord[1]] = [ETAT[num], num]
    print (plateau[coord[0]][coord[1]])



def debut():
    dixieme_hauteur = cfg.hauteur_fenetre / 10
    dixieme_largeur = cfg.largeur_fenetre / 10

    boutons = init_boutons()

    lignes = fltk.boite_texte(dixieme_largeur, dixieme_hauteur*3.2, "Courier 20", "25", "center" )
    colonnes = fltk.boite_texte(dixieme_largeur, dixieme_hauteur*5.1, "Courier 20", "25", "center" )

    #A mieux positionner
    

    while True:
        fltk.efface_tout()
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        graphiques.background("#3f3e47")
        click = boutons.dessiner_boutons(tev)


        # inp = fltk.get_texte(boite)
        # print(inp)

        if tev == 'Quitte':
            fltk.ferme_fenetre()
            exit()

        if tev == "ClicGauche":
            if click not in {None}:
                nb_lignes = lignes.get()
                nb_colonnes = colonnes.get()

                if type(nb_lignes) != int or type(nb_colonnes)!= int:
                    nb_lignes = int(nb_lignes)
                    nb_colonnes = int(nb_colonnes)
                    if nb_lignes * nb_colonnes <= 0:
                        init_boutons(True)
                    else:
                        lignes.destroy()
                        colonnes.destroy()
                        fltk.ferme_fenetre()
                        fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre, "Ricosheep")
                        return main(nb_lignes, nb_colonnes)
                    
                else:
                    boutons = init_boutons(True)

        fltk.mise_a_jour()

def main(lignes, colonnes):
    boutons, plateau = init_boutons_grille(colonnes, lignes)

    while True:
        fltk.efface_tout()

        graphiques.background("#3f3e47")
        boutons.grille.draw()
    
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        
        click = boutons.dessiner_boutons(tev) 
        if tev == "Quitte":
            fltk.ferme_fenetre()
            exit()

        if tev == "Touche":
            touche = fltk.touche(ev)
            print(touche)

            if touche == "t":
                return plateau

        if tev == "ClicGauche":
            if click not in {None}:
                coord = click.split()
                coord[0], coord[1] = int(coord[0]), int(coord[1])
                change_case(plateau, coord)

        if tev == "ClicDroit":
            print(plateau)
            return plateau



        fltk.mise_a_jour()



if __name__ == "__main__":
    fltk.cree_fenetre(500, 500)
    ligne, colonne = debut()
    fltk.ferme_fenetre()
    fltk.cree_fenetre(500, 500)
    print(main(ligne, colonne))