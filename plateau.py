from typing import List, Tuple, Dict
from pprint import pprint
from mouton import Mouton
from grille import Grille
import fltk


class Plateau:
    # Utiliser __slots__ pour les gains de mémoire...
    # Il faudrait que troupeau soit un set...

    grille:       Grille
    nb_colonnes:  int
    nb_lignes:    int
    troupeau:     List[Mouton]
    env:          Dict[str, set] # Contient les positions des buissons et des touffes
    images:       Dict[str, object]
    taille_image: float
    __slots__ = tuple(__annotations__)
    
    def __hash__(self):
        return hash(tuple(sorted(self.troupeau)))

    def __eq__(self, other):
        return sorted(self.troupeau) == sorted(other.troupeau)

    def __init__(self, gridfile: str, test_mode=False):
        self.grid_parse(gridfile)
        if test_mode: return

        self.grille = Grille(self.nb_colonnes, self.nb_lignes)
        self.taille_image = self.grille.largeur_case * 0.8

        global images
        images = {
            "buissons" : fltk.box_image('media/bush.png',  (self.taille_image,)),
            "touffes"  : fltk.box_image('media/grass.png', (self.taille_image,)),
            "mouton"   : fltk.box_image('media/sheep.png', (self.taille_image,)),
            "heureux"  : fltk.box_image('media/sheep_grass.png', (self.taille_image,))
        }

    def grid_parse(self, file: str):
        self.troupeau = []
        self.env = {'buissons': set(), 'touffes': set()}
        self.nb_lignes = 0
        with open(file) as f:
            for line in f.readlines():
                self.nb_colonnes = 0
                for char in line:
                    pos = (self.nb_lignes, self.nb_colonnes)
                    if char in 'B':
                        self.env['buissons'].add(pos)
                    elif char == 'G':
                        self.env['touffes'].add(pos)
                    elif char == 'S':
                        self.troupeau.append(Mouton(*pos))
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
            heureux = 'heureux' if m in self.env['touffes'] else 'mouton'
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
                 not (y, x) in self.env['buissons'] and
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
        if direction in {"Down", "Right"}:
            self.troupeau.sort(reverse=True)
        elif direction in {"Up", "Left"}:
            self.troupeau.sort(reverse=False)

    def isGagne(self):
        occupe = 0
        for herbe in self.env['touffes']:
            for mouton in self.troupeau:
                if mouton.x == herbe[1] and mouton.y == herbe[0]:
                    occupe += 1
        return occupe == len(self.env['touffes'])
