from dataclasses import dataclass
from typing import List, Tuple
from mouton import Mouton
import fltk
import cfg

@dataclass
class Case:
    ax: int
    ay: int
    bx: int
    by: int
    ax_image: int
    ay_image: int
    contenu: str # 'G' ou 'B' ou None PAS de moutons !
    image = None

class Plateau:
    # - Mettre ailleurs les images que dans Cases
    # car cela empêche l'utilisation de deepcopy()
    # nécessaire pour le "Undo/Redo"
    # Utiliser __slots__ pour les gains de mémoire...
    img_buisson = None
    img_herbe   = None
    img_mouton  = None
    
    def __init__(self,
                 raw_plateau: List[List],
                 raw_moutons: Tuple[Tuple[int, int]]):
        self.troupeau     = self.genererMoutons(raw_moutons)

        self.nb_colonne  = len(raw_plateau[0])
        self.nb_ligne    = len(raw_plateau)
        self.cases, self.box_image = self.genererCases(raw_plateau, 0.8)
        
        self.img_buisson = fltk.box_image('media/bush.png',  (self.box_image,))
        self.img_herbe   = fltk.box_image('media/grass.png', (self.box_image,))
        self.img_mouton  = fltk.box_image('media/sheep.png', (self.box_image,))
        self.imagerCases()
        
    def genererCases(self, raw_plateau: List[List], proportion: int):
        """
        Initialise une liste d'objets ``Cases``, dont les coordonnées
        ont été adaptées à la taille de la fenêtre.

        :param List raw_plateau: Liste de liste brute du fichier niveau
        :param float proportion: Proportion des images par rapport aux cases
        :return: Tuple composé d'une liste de ``Cases`` et la taille
        (carré) en pixels des cases générées.
        """
    
        cases = []
    
        marge_largeur = cfg.largeur_fenetre * 0.05
        marge_hauteur = cfg.hauteur_fenetre * 0.05

        taille_case = min(
            (cfg.largeur_fenetre - marge_largeur)/self.nb_colonne,
            (cfg.hauteur_fenetre - marge_hauteur)/self.nb_ligne
        )
        taille_image = taille_case * proportion
        marge = (taille_case - taille_image) / 2
        
        view_ax = (cfg.largeur_fenetre - taille_case * self.nb_colonne)/2
        view_ay = (cfg.hauteur_fenetre - taille_case * self.nb_ligne)/2
        
        for j in range(self.nb_ligne):
            ligne = []
            for i in range(self.nb_colonne):
                ax = view_ax + (i * taille_case)
                ay = view_ay + (j * taille_case)
                ligne.append(
                    Case(
                        ax=ax,
                        ay=ay,
                        bx=ax + taille_case,
                        by=ay + taille_case,
                        ax_image=ax + marge,
                        ay_image=ay + marge,
                        contenu=raw_plateau[j][i]
                    )
                )
    
            cases.append(ligne)
    
        return cases, taille_image

    def genererMoutons(self, moutons: List[Tuple[int, int]]):
        """
        Génère une liste d'objets ``Mouton``s

        :param List moutons: Sequence de tuple de moutons
        de coordonnes ``(y, x)``
        :return List: Liste d'objets Mouton
        """
        return [Mouton(mouton[0], mouton[1]) for mouton in moutons]

    def imagerCases(self):
        """
        Ajoute les images fixes (buisson, herbes) dans les
        cases de la liste ``cases`` de l'instance de la classe.
        """
        for ligne in self.cases:
            for case in ligne:
                if case.contenu == 'B':
                    case.image = self.img_buisson
                elif case.contenu == 'G':
                    case.image = self.img_herbe

    def draw_grid(self):
        """
        Dessine les cases du plateau, et affiche le images
        buisson et herbe.
        """
        for ligne in self.cases:
            for case in ligne:
                fltk.rectangle(
                    case.ax,case.ay,
                    case.bx,case.by,
                    'white'
                )
                if case.contenu is not None:
                    fltk.afficher_image(
                        case.ax_image, case.ay_image,
                        case.image, ancrage='nw'
                    )
            
    def draw_moutons(self):
        """
        Dessine les moutons.
        """
        
        for mouton in self.troupeau:
            case = self.cases[mouton.y][mouton.x]
            fltk.afficher_image(case.ax_image, case.ay_image,
                                self.img_mouton, ancrage='nw'
            )

    def isPosMouton(self, x, y):
        for mouton in self.troupeau:
            if mouton.x == x and mouton.y == y:
                return False
        else:
            return True

            
    def isPositionValid(self, x: int, y: int):
        """
        Détermine si la position indiquée par ``x``
        et ``y`` n'est pas en dehors du plateau, et
        si la case est vide ou est une touffe d'herbe.
        """
        moutonposValid = self.isPosMouton(x, y)
        return (0 <= y < self.nb_ligne and
                (0 <= x < self.nb_colonne) and
                 self.cases[y][x].contenu != 'B'
                 and moutonposValid)

    def deplace_moutons(self, direction: str):
        self.troupeau = self.tri_moutons(direction)
        for mouton in self.troupeau:
            mouton.deplace(direction, self)

    def tri_moutons(self, direction):
        if direction == "Up" or direction == "Down":
            self.troupeau.sort(key=self.tri_y)
            if direction == "Down":
                self.troupeau.reverse()    

        elif direction == "Left" or direction == "Right":
            self.troupeau.sort(key=self.tri_x)
            if direction == "Right":
                self.troupeau.reverse()
                
        return self.troupeau


    def tri_y(self, troupeau):
        return troupeau.y

    def tri_x(self, troupeau):
        return troupeau.x
