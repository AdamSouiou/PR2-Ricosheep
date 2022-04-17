from dataclasses import dataclass
from pprint import pprint
from typing import List, Tuple
from mouton import Mouton
from grille import Grille
import fltk
import cfg


class Plateau:
    # Utiliser __slots__ pour les gains de mémoire...
    # Il faudrait que troupeau soit un set...
    def __hash__(self):
        return hash(tuple(sorted(self.troupeau)))

    def __eq__(self, other):
        if not isinstance(self, type(other)):
            raise TypeError("Une égalité entre un plateau et\
                             un autre type d'objet à été tentée")
        return sorted(self.troupeau) == sorted(other.troupeau)

    def __init__(self, gridfile: str):
        self.grid_parse(gridfile)
        self.env = {'B' : self.buissons, 'G': self.touffes}
        self.troupeau = self.genererMoutons(self.raw_moutons)

        self.grille = Grille(self.nb_colonnes, self.nb_lignes)
        self.taille_image = self.grille.largeur_case * 0.8

        global images
        images = {
            "B" : fltk.box_image('media/bush.png',  (self.taille_image,)),
            "G" : fltk.box_image('media/grass.png', (self.taille_image,)),
            "M" : fltk.box_image('media/sheep.png', (self.taille_image,)),
            "E" : fltk.box_image('media/sheep_grass.png', (self.taille_image,))
        }

    def genererMoutons(self, moutons: List[Tuple[int, int]]):
        """
        Génère une liste d'objets ``Mouton``s

        :param List moutons: Sequence de tuple de moutons
        de coordonnes ``(y, x)``
        :return List: Liste d'objets Mouton
        """
        return [Mouton(mouton[1], mouton[0]) for mouton in moutons]

    def grid_parse(self, file: str):
        self.raw_moutons, self.touffes, self.buissons = [], set(), set()
        self.nb_lignes = 0
        with open(file) as f:
            for line in f.readlines():
                self.nb_colonnes = 0
                for char in line:
                    pos = (self.nb_lignes, self.nb_colonnes)
                    if char in 'B':
                        self.buissons.add(pos)
                    elif char == 'G':
                        self.touffes.add(pos)
                    elif char == 'S':
                        self.raw_moutons.append(pos)
                    self.nb_colonnes += 1
                self.nb_lignes += 1

    affiche = lambda self, case, img: fltk.afficher_image(
                case.centre_x,
                case.centre_y,
                img, ancrage='center'
    )
    
    def draw(self):
        self.grille.draw()
        for name, elements in self.env.items():
            for y,x in elements:
                case = self.grille.cases[y][x]
                self.affiche(case, images[name])
        for m in self.troupeau:
            heureux = 'E' if m in self.touffes else 'M'
            case = self.grille.cases[m.y][m.x]
            self.affiche(case, images[heureux])   

    def isNotPosMouton(self, x, y):
        for mouton in self.troupeau:
            if mouton.x == x and mouton.y == y:
                return False
        return True

            
    def isPositionValid(self, x: int, y: int):
        """
        Détermine si la position indiquée par ``x``
        et ``y`` n'est pas en dehors du plateau, et
        si la case est vide ou est une touffe d'herbe.
        """
         
        return (0 <= y < self.nb_lignes and
                (0 <= x < self.nb_colonnes) and
                 not (y, x) in self.buissons and
                  self.isNotPosMouton(x, y))

    def deplace_moutons(self, direction: str):
        self.tri_moutons(direction)
        for mouton in self.troupeau:
            mouton.deplace(direction, self)

    def tri_moutons(self, direction):
        """
        Trie les moutons de sorte que le mouton le plus près
        du mur de la direction demandée soit le premier à être déplacé.
        """
        if direction in {"Down","Right"}:
            self.troupeau.sort(reverse=True)
        else:
            self.troupeau.sort(reverse=False)

    def isGagne(self):
        occupe = 0
        for herbe in self.touffes:
            for mouton in self.troupeau:
                if mouton.x == herbe[1] and mouton.y == herbe[0]:
                    occupe += 1
        return occupe == len(self.touffes)
