import fltk
import cfg
import son
from bouton import Boutons
from grille import Grille
from collections import namedtuple as nt
from os import PathLike
from pprint import pprint

namedtuple = lambda nom, **kwargs : nt(nom, kwargs)(*kwargs.values())


def background(couleur: str) -> None:
    """
    Crée un arrière plan uni

    :param str couleur: Couleur du fond
    """

    fltk.rectangle(
        0, 0,
        cfg.largeur_fenetre, cfg.hauteur_fenetre,
        remplissage=couleur
    )

    return None

def image_grille(ax: int, ay: int, bx: int, by: int,
                 fichier: PathLike, grille: Grille):
    """
    Ouvre et affiche une image en respectant les coordonées dans
    la grille.
    """
    case_a = grille.cases[ay][ax]
    case_b = grille.cases[by][bx]
    largeur, hauteur = (case_b.bx - case_a.ax,
                        case_b.by - case_a.ay)
    return namedtuple(
        'Image',
        image=box_image(
            fichier,
            (largeur, hauteur)
        ),
        centre_x=case_a.ax + (largeur // 2),
        centre_y=case_a.ay + (hauteur // 2))


def game_over_init(text: str, hexcode: str, grille: Grille) -> Boutons:
    """
    Initialise les boutons de fin de jeu selon le texte, la couleur et la grille.
    """
    boutons = Boutons((20,20), grille_base=grille)
    boutons.cree_bouton_texte(3, 6, 12, 13, text, arrondi=0.5, couleur_texte=hexcode)
    boutons.init()
    return boutons

def demande_affichage(grille_jeu: Grille):
    """
    Crée une invite au-dessus du plateau demandant à l'utilisateur
    si il souhaite afficher graphiquement la solution
    :param grille_jeu: Grille des boutons du jeu, selon
    laquelle sera placé l'invite.
    """
    demande = Boutons((0,), grille_base=grille_jeu) # (20,23)
    demande.cree_bouton_texte(2, 6, 13, 9, 'Afficher la solution')
    demande.cree_bouton_simple(2, 10, 7, 11, 'Oui')
    demande.cree_bouton_simple(8, 10, 13, 11, 'Non')
    demande.init()
    demande.dessiner_boutons()
    #demande.grille.draw()
    fltk.mise_a_jour()
    while True:
        ev = fltk.attend_ev()
        click = demande.nom_clic(ev)
        if click == 'Oui':
            son.sound('MenuAccept')
            return True
        elif click == 'Non':
            son.sound('MenuBleep')
            return False
    
    

affiche_env_element = lambda case, img: fltk.afficher_image(
        case.centre_x,
        case.centre_y,
        img, ancrage= "center")


def affiche_case(x, y, grille, img):
    """
    Affiche le contenu de la case donné avec l'image donné.
    """
    case = grille.cases[y][x]
    affiche_env_element(case, img)


def calcul_taille_image(taille_image: tuple, taille_box: tuple, marge=0):
    """
    Calcule le coefficient d'agrandissement ou de réduction
    afin de préserver le ratio à appliquer à l'image,
    afin d'optimiser l'espace de la box.
    
    :param tuple taille_image: Tuple représentant la largeur et
    la hauteur de l'image
    :param tuple taille_box: Tuple représentant la largeur et
    la hauteur de la box qui contiendra l'image
    :param float marge: Marge à appliquer au minimum sur les bords
    
    """

    largeur_image, hauteur_image = taille_image
    marge /= 2
    largeur_box, hauteur_box = taille_box[0] - marge, taille_box[1] - marge

    return min(largeur_box/largeur_image, hauteur_box/hauteur_image)


def box_image(fichier, box, marge=0):
    """
    Renvoie une image satisfaisant les contraintes de la box et
    de la marge sans étirement.
    
    :param str fichier: Nom du fichier
    :param tuple box: tuple de la forme : ``(largeur, hauteur)`` pour
    une box rectangulaire, ou ``(carre,)`` (tuple de longueur 1) pour
    une box carrée.
    :param float marge: Nombre de pixels minimum entre les bords de
    l'image et la box.

    :return Image: Objet image
    """
    if len(box) == 1:
        box = (box[0], box[0])

    return fltk.redimensionner_image(
        fichier,
        calcul_taille_image(
            fltk.taille_image(fichier),
            box,
            marge
        )
    )

def close() -> None:
    """
    Ferme la fenêtre fltk et quitte l'exécution de python
    """
    fltk.ferme_fenetre()
    exit()