import fltk
import cfg

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

def victory():
    marge = [cfg.largeur_fenetre/10, cfg.hauteur_fenetre/3]
    fltk.rectangle(
        marge[0], marge[1],
        cfg.largeur_fenetre - marge[0],
        cfg.hauteur_fenetre - marge[1],
        remplissage="white")

    fltk.texte(cfg.largeur_fenetre/2, cfg.hauteur_fenetre/2, "C'est gagné !!",
      police="Courier", taille=30, couleur="green",
      ancrage='center')

def affiche_case(x, y, grille, img):
    case = grille.cases[y][x]
    fltk.afficher_image(
            case.centre_x,
            case.centre_y,
            img, ancrage='center'
    )