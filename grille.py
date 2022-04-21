from dataclasses import dataclass
import cfg
import fltk


@dataclass
class Case:
    ax: int
    ay: int
    bx: int
    by: int
    centre_x: int
    centre_y: int


class Grille:
    def __init__(self, nb_colonne: int, nb_ligne: int,
                 marge_largeur=0.95, marge_hauteur=0.95,
                 grille_base=None,
                 grille_pos=(0, 0, cfg.largeur_fenetre, cfg.hauteur_fenetre),
                 carre=True):

        """
        Objet Grille, permettant de dessiner... une grille.
        :param float marge_largeur: Proportion en largeur de la grille
        dans la box définie par ``grille_pos``
        :param float marge_hauteur: Proportion en hauteur de la grille
        dans la box définie par ``grille_pos``
        :param Grille grille_base: Si une grille est reçue,
        elle sera utilisée pour définir la position absolue de la nouvelle grille
        par rapport à celle-ci et les coordonnées données par ``grille_pos``
        :param tuple grille_pos: Position absolue (par rapport à la fenêtre) si
        ``grille_base`` vaut ``None``, sinon position par rapport aux coordonnées
        des cases de ``grille_base``.
        :param bool carre: Si ``True`` adapte la taille de la grille,
        de sorte que les cases restent carrées.
        """

        if grille_base is not None:
            self.view_ax, self.view_ay = grille_base.getAbsoluteCoordsTL(
                grille_pos[0], grille_pos[1]
            )
            self.view_bx, self.view_by = grille_base.getAbsoluteCoordsBR(
                grille_pos[2], grille_pos[3]
            )
        else:
            self.view_ax, self.view_ay = grille_pos[0], grille_pos[1]
            self.view_bx, self.view_by = grille_pos[2], grille_pos[3]
        
        self.marge_largeur = marge_largeur
        self.marge_hauteur = marge_hauteur
        self.nb_colonne = nb_colonne
        self.nb_ligne = nb_ligne
        self.carre = carre
        self.genererCases()
        
    def genererCases(self):
        """
        Initialise une liste d'objets ``Cases``, dont les coordonnées
        ont été adaptées à la taille de la fenêtre.

        :return: Tuple composé d'une liste de ``Cases`` et la taille
        (carré) en pixels des cases générées.
        """
        largeur_interieur = (self.view_bx - self.view_ax)*self.marge_largeur
        hauteur_interieur = (self.view_by - self.view_ay)*self.marge_hauteur
        
        self.cases = []

        self.largeur_case, self.hauteur_case = (
            largeur_interieur/self.nb_colonne,
            hauteur_interieur/self.nb_ligne
        )
        
        if self.carre:
            m = min(self.largeur_case, self.hauteur_case)
            self.largeur_case, self.hauteur_case = m, m

        self.view_ax += ((self.view_bx - self.view_ax) - self.largeur_case*self.nb_colonne)//2
        self.view_ay += ((self.view_by - self.view_ay) - self.hauteur_case*self.nb_ligne)//2

        print(self.view_ax, self.view_ay)
        
        for j in range(self.nb_ligne):
            ligne = []
            for i in range(self.nb_colonne):
                ax = self.view_ax + (i * self.largeur_case)
                ay = self.view_ay + (j * self.hauteur_case)
                
                ligne.append(
                    Case(
                        ax=ax,
                        ay=ay,
                        bx=ax + self.largeur_case,
                        by=ay + self.hauteur_case,
                        centre_x=ax + self.largeur_case//2,
                        centre_y=ay + self.hauteur_case//2,
                    )
                )
    
            self.cases.append(ligne)

    def draw(self, callback=None):
        """
        Dessine les cases
        """
        
        for y, ligne in enumerate(self.cases):
            for x, case in enumerate(ligne):
                fltk.rectangle(
                    case.ax,case.ay,
                    case.bx,case.by,
                    'white'
                )
                if callback is not None:
                    callback(case, x, y)
    
    def getAbsoluteCoordsTL(self, x_case: int, y_case: int):
        return (self.cases[y_case][x_case].ax,
                self.cases[y_case][x_case].ay)

    def getAbsoluteCoordsBR(self, x_case: int, y_case: int):
        return (self.cases[y_case][x_case].bx,
                self.cases[y_case][x_case].by)