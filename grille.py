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
    def __init__(self, nb_colonne: int, nb_ligne: int):
        self.nb_colonne = nb_colonne
        self.nb_ligne = nb_ligne
        self.cases, self.taille_case = self.genererCases()
        
    def genererCases(self, carre=False, marge_largeur=0.95, marge_hauteur=0.95):
        """
        Initialise une liste d'objets ``Cases``, dont les coordonnées
        ont été adaptées à la taille de la fenêtre.

        :return: Tuple composé d'une liste de ``Cases`` et la taille
        (carré) en pixels des cases générées.
        """
        
        cases = []

        taille_case = min(
            (cfg.largeur_fenetre * marge_largeur)/self.nb_colonne,
            (cfg.hauteur_fenetre * marge_hauteur)/self.nb_ligne
        )

        view_ax = (cfg.largeur_fenetre - taille_case * self.nb_colonne)//2
        view_ay = (cfg.hauteur_fenetre - taille_case * self.nb_ligne)//2
        
        for j in range(self.nb_ligne):
            ligne = []
            for i in range(self.nb_colonne):
                ax = view_ax + (i * taille_case)
                ay = view_ay + (j * taille_case)
                centre = taille_case/2
                
                ligne.append(
                    Case(
                        ax=ax,
                        ay=ay,
                        bx=ax + taille_case,
                        by=ay + taille_case,
                        centre_x=ax + centre,
                        centre_y=ay + centre,
                    )
                )
    
            cases.append(ligne)
    
        return cases, taille_case

    def draw(self, affiche_case=None):
        """
        Dessine les cases
        """
        for ligne in self.cases:
            for case in ligne:
                fltk.rectangle(
                    case.ax,case.ay,
                    case.bx,case.by,
                    'white'
                )