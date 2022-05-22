import fltk
import cfg
from bouton import Boutons
from grille import Grille
from collections import namedtuple as nt
from os import PathLike
from pprint import pprint
from functools import partial
import solveur

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


def game_over_init(text, hexcode, grille):
    boutons = Boutons((20,20), grille_base=grille)
    boutons.cree_bouton_texte(3, 6, 12, 13, text, arrondi=0.5, couleur_texte=hexcode)
    boutons.init()
    return boutons


def gen_invite(demande: str, cas1: str, cas2: str, grille_base):
    """
    Génère une invite à deux choix, et retourne une instance
    de boutons.
    """
    invite = Boutons((20,23), grille_base=grille_base)
    invite.cree_bouton_texte(2, 6, 13, 9, demande)
    invite.cree_bouton_simple(2, 10, 7, 11, cas1)
    invite.cree_bouton_simple(8, 10, 13, 11, cas2)
    invite.init()
    return invite


def demande_affichage(grille_jeu: Grille):
    """
    Crée une invite au-dessus du plateau demandant à l'utilisateur
    si il souhaite afficher graphiquement la solution
    :param grille_jeu: Grille des boutons du jeu, selon
    laquelle sera placé l'invite.
    """
    invite = gen_invite("Afficher la solution", "Oui", "Non", grille_jeu)
    invite.dessiner_boutons()
    fltk.mise_a_jour()
    while True:
        ev = fltk.attend_ev()
        click = invite.nom_clic(ev)
        if click == 'Oui':
            return True
        elif click == 'Non':
            return False


def demande_profondeur(grille_jeu: Grille):
    """
    Invite demandant à l'utilisateur quel solveur en
    profondeur il souhaite (itératif ou récursif)
    :param grille_jeu: Grille des boutons du jeu, selon
    laquelle sera placé l'invite.
    """
    invite = gen_invite("Choix algorithme :", "Récursif", "Itératif", grille_jeu)
    invite.dessiner_boutons()
    fltk.mise_a_jour()
    while True:
        ev = fltk.attend_ev()
        click = invite.nom_clic(ev)
        if click == "Récursif":
            return solveur.profondeur
        elif click == "Itératif":
            return partial(solveur.iteratif, largeur=False)


affiche_env_element = lambda case, img: fltk.afficher_image(
        case.centre_x,
        case.centre_y,
        img, ancrage= "center")


def affiche_case(x, y, grille, img):
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

def close():
    fltk.ferme_fenetre()
    exit()