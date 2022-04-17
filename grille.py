from dataclasses import dataclass
from typing import List, Tuple
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
                 marge_largeur=0.95, marge_hauteur=0.95, carre=True):
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
        
        self.cases = []

        self.largeur_case, self.hauteur_case = (
            (cfg.largeur_fenetre * self.marge_largeur)/self.nb_colonne,
            (cfg.hauteur_fenetre * self.marge_hauteur)/self.nb_ligne
        )
        
        if self.carre:
            m = min(self.largeur_case, self.hauteur_case)
            self.largeur_case, self.hauteur_case = m, m

        self.view_ax = (cfg.largeur_fenetre - self.largeur_case * self.nb_colonne)//2
        self.view_ay = (cfg.hauteur_fenetre - self.hauteur_case * self.nb_ligne)//2
        self.view_bx = cfg.largeur_fenetre - self.view_ax
        self.view_by = cfg.hauteur_fenetre - self.view_ay
        
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