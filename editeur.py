from typing import List, Tuple
from bouton import Boutons
from grille import Grille
from plateau import Plateau
from graphiques import box_image, affiche_env_element, close
from pprint import pprint
from copy import deepcopy
import graphiques
import cfg
import fltk
import solveur
import creation_niveaux
import son


ETAT = ('_', "B", "G", "S")


def init_boutons_grille(nb_lignes: int, nb_colonnes: int) -> Tuple[Boutons, List]:
    """
    Initialise les boutons ainsi qu'une liste des boutons invisibles.
    """
    liste = []
    boutons = Boutons((nb_lignes, nb_colonnes))
    for colonne in range(nb_colonnes):
        temp = []
        for ligne in range(nb_lignes):
            temp.append('_')
            boutons.cree_bouton_invisible(ligne, colonne, ligne, colonne,
                                          f"{colonne} {ligne}")
        liste.append(temp)
    return boutons, liste

def change_case(plateau: Plateau, coord: Tuple[int, int]) -> None:
    """
    Change l'état de la case du plateau aux coordonnés.
    """
    num = (ETAT.index(plateau[coord[0]][coord[1]]) + 1 ) % 4
    plateau[coord[0]][coord[1]] = ETAT[num]

def initplateau(grille: Grille):
    """
    Initialise les images du plateau à partir d'une grille fournie.
    """
    global images
    taille_image = grille.largeur_case * 0.8
    images = {
            "B" : box_image('media/images/bush.png',  (taille_image,)),
            "G" : box_image('media/images/grass.png', (taille_image,)),
            "S" : box_image('media/images/sheep.png', (taille_image,)),
        }


def draw(plateau: Plateau, grille: Grille) -> None:
    """
    Dessine le plateau et la grille dans la fenêtre fltk.
    """
    grille.draw()

    for ligne in range(len(plateau)):
        case = grille.cases[ligne]
        for colonne in range(len(plateau[0])):
            if plateau[ligne][colonne] != '_':
                affiche_env_element(case[colonne], images[plateau[ligne][colonne]])

def test(carte: List[List[str]],
         editeur: bool = True,
         largeur: bool = True) -> Tuple[bool, List[str]]:
    """
    Transforme la carte en un plateau et cherche une solution.
    Renvoie un tuple avec s'il existe une solution, et la solution.
    """
    plateau = Plateau(carte)
    chemin, _ = solveur.iteratif(deepcopy(plateau), largeur=largeur)

    if chemin is None:
        if editeur == True:
            print("Ton niveau n'a pas de solutions ! Recommence !")
            return False
        return False, []
    else:
        if editeur == True:
            print(f"La longueur du chemin est de {len(chemin)}")
            return True
        return True, chemin


def debut():
    boutons = Boutons((10,10))
    boutons.cree_bouton_texte(1, 2, 5, 2, "Nombre de lignes :", arrondi=0.75)
    boutons.cree_bouton_texte(1, 4, 5, 4, "Nombre de colonnes :", arrondi=0.75)
    boutons.entree_texte(7, 2, 8, 2, "lignes")
    boutons.entree_texte(7, 4, 8, 4, "colonnes")
    boutons.cree_bouton_simple(2, 6, 7, 6, "Valider", arrondi = 1)
    entiers_positifs = "Veuillez insérer des entiers positifs !"
    boutons.cree_bouton_texte(1, 8, 8, 8, entiers_positifs,
                              invisible=True, couleur_texte='red')
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
            close()
        if tev == "Touche":
            if fltk.touche(ev) == "Escape":
                boutons.destroy_entree_textes()
                return

        if tev == "ClicGauche":
            if click not in {None}:
                son.sound('MenuAccept')
                nb_lignes = boutons.entrees_texte['lignes'].get()
                nb_colonnes = boutons.entrees_texte['colonnes'].get()

                if nb_lignes.isdigit() and nb_colonnes.isdigit():
                    nb_lignes = int(nb_lignes)
                    nb_colonnes = int(nb_colonnes)
                    if not nb_lignes * nb_colonnes == 0:
                        return main(nb_lignes, nb_colonnes)
                else:
                    boutons.boutons[entiers_positifs].invisible = False

        fltk.mise_a_jour()

def main(lignes, colonnes):
    boutons, plateau = init_boutons_grille(colonnes, lignes)
    initplateau(boutons.grille)
    ev = None
    
    while True:

        fltk.efface_tout()
        graphiques.background("#3f3e47")
        boutons.dessiner_boutons(ev)
        draw(plateau, boutons.grille)
        
        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        click = boutons.nom_clic(ev)

        if tev == "Quitte":
            boutons.destroy_entree_textes()
            close()

        if tev == "Touche":
            touche = fltk.touche(ev)
            if touche == "Return":
                son.sound('MenuAccept')
                if test(plateau):
                    return creation_niveaux.menu(plateau)

            if touche == "Escape":
                boutons.destroy_entree_textes()
                return

        if tev == "ClicGauche":
            if click is not None:
                son.sound('Sheep')
                coord = click.split()
                coord[0], coord[1] = int(coord[0]), int(coord[1])
                change_case(plateau, coord)

        fltk.mise_a_jour()
