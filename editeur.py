from bouton import Boutons
from plateau import Plateau
from graphiques import box_image

import graphiques
import cfg
import fltk
import solveur
import creation_niveaux
import son


ETAT = [None, "B", "G", "S"]


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
            temp.append(None)
            boutons.cree_bouton_invisible(ligne, colonne, ligne, colonne, f"{colonne} {ligne}")
        Liste.append(temp)
    return boutons, Liste

def change_case(plateau, coord):
    num = (ETAT.index(plateau[coord[0]][coord[1]]) + 1 ) % 4
    plateau[coord[0]][coord[1]] = ETAT[num]

def initplateau(grille):
    global images
    taille_image = grille.largeur_case * 0.8
    images = {
            "B" : box_image('media/bush.png',  (taille_image,)),
            "G" : box_image('media/grass.png', (taille_image,)),
            "S" : box_image('media/sheep.png', (taille_image,)),
        }


affiche_env_element = lambda case, img: fltk.afficher_image(
        case.centre_x,
        case.centre_y,
        img, ancrage= "center")

def draw(plateau, grille):
    grille.draw()

    for ligne in range(len(plateau)):
        case = grille.cases[ligne]
        for elem in range(len(plateau[0])):
            if plateau[ligne][elem] != None:
                affiche_env_element(case[elem], images[plateau[ligne][elem]])

def test(carte):
    plateau = Plateau(carte, editeur = carte)
    pos_tmp = solveur.tri_copy(plateau.troupeau)
    chemin, _ = solveur.profondeur(plateau)

    if chemin == None:
        print("Pas de solutions, chacal!, recommence ton niveau")
        return False
    else:
        solveur.restore(plateau.troupeau, pos_tmp)
        print(chemin)
        print("Le solveur a bon? :", solveur.test(chemin, plateau, 0))
        # print(chemin)
        print(f"La longueur du chemin est de {len(chemin)}")
        return True


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

        if tev == 'Quitte':
            fltk.ferme_fenetre()
            exit()

        if tev == "ClicGauche":
            if click not in {None}:
                son.sound('MenuOk')
                nb_lignes = lignes.get()
                nb_colonnes = colonnes.get()

                if nb_lignes.isdigit() and nb_colonnes.isdigit():
                    nb_lignes = int(nb_lignes)
                    nb_colonnes = int(nb_colonnes)
                    if nb_lignes * nb_colonnes == 0:
                        boutons = init_boutons(True)
                    else:
                        lignes.destroy()
                        colonnes.destroy()
                        fltk.resetfocus()

                        return main(nb_lignes, nb_colonnes)
                    
                else:
                    boutons = init_boutons(True)

        fltk.mise_a_jour()

def main(lignes, colonnes):
    boutons, plateau = init_boutons_grille(colonnes, lignes)
    initplateau(boutons.grille)

    while True:
        fltk.efface_tout()

        graphiques.background("#3f3e47")
        draw(plateau, boutons.grille)
    
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
                son.sound('MenuOk')
        
                if test(plateau):
                    return creation_niveaux.menu(plateau)

        if tev == "ClicGauche":
            if click not in {None}:
                son.sound('Sheep')
                coord = click.split()
                coord[0], coord[1] = int(coord[0]), int(coord[1])
                change_case(plateau, coord)

        fltk.mise_a_jour()



if __name__ == "__main__":
    fltk.cree_fenetre(500, 500)
    debut()