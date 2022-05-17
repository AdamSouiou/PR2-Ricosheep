import fltk
import cfg
from bouton import Boutons

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

def logo():
    image = box_image('media/Logo_ricosheep.png', (cfg.largeur_fenetre*0.7, cfg.largeur_fenetre*0.7*(1/3)))
    return image

def game_over_init(text, hexcode, second):
    boutons = Boutons((10,10))
    boutons.cree_bouton_texte(2, 3, 7, 5, text, arrondi=0.5)
    boutons.boutons[text].couleur_texte = hexcode
    boutons.cree_bouton_simple(3, 7, 6, 7, second, arrondi=1)
    boutons.init()
    return boutons

def affiche_case(x, y, grille, img):
    case = grille.cases[y][x]
    fltk.afficher_image(
            case.centre_x,
            case.centre_y,
            img, ancrage='center'
    )


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