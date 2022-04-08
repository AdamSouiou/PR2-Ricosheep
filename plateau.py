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
    x: int
    y: int

class Plateau:
    def __init__(self, nb_colonne: int, nb_ligne: int):
        self.nb_colonne = nb_colonne
        self.nb_ligne = nb_ligne
        self.cases, self.taille_case = self.generer()
        
    def generer(self):
        """
        Initialise une liste d'objets ``Cases``, dont les coordonnées
        ont été adaptées à la taille de la fenêtre.
        
        :return: Tuple composé d'une liste de ``Cases`` et la taille
        (carré) en pixels des cases générées.
        """
    
        cases = []
    
        marge_largeur = cfg.largeur_fenetre*0.05
        marge_hauteur = cfg.hauteur_fenetre*0.05

        taille_case = min(
            (cfg.largeur_fenetre - marge_largeur)/self.nb_colonne,
            (cfg.hauteur_fenetre - marge_hauteur)/self.nb_ligne
        )
        
        view_ax = (cfg.largeur_fenetre - taille_case * self.nb_colonne)/2
        view_ay = (cfg.hauteur_fenetre - taille_case * self.nb_ligne)/2
        # view_bx = view_ax + self.nb_colonne*taille_case
        # view_by = view_ay + self.nb_ligne*taille_case
        
        for j in range(self.nb_ligne):
            ligne = []
            for i in range(self.nb_colonne):
                ligne.append(
                    Case(
                        ax=view_ax  + i * taille_case,
                        ay=view_ay  + j * taille_case,
                        bx=(view_ax + i * taille_case) + taille_case,
                        by=(view_ay + j * taille_case) + taille_case,
                        x=i,
                        y=j
                    )
                )
    
            cases.append(ligne)
    
        return cases, taille_case

    def draw(self):
        """
        Dessines les cases du plateau, tout simplement.
        """
        for ligne in self.cases:
            for case in ligne:
                fltk.rectangle(
                    case.ax,
                    case.ay,
                    case.bx,
                    case.by,
                    'white'
                )
