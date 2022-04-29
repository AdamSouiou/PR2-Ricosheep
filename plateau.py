from typing import List, Tuple, Dict, Set
from pprint import pprint
from mouton import Mouton
from graphiques import affiche_env_element
from grille import Grille
from copy import deepcopy
import fltk
import cfg


class Plateau:
    # Utiliser __slots__ pour les gains de mémoire...
    # Il faudrait que troupeau soit un set...

    grille:             Grille
    nb_colonnes:        int
    nb_lignes:          int
    troupeau:           List[Mouton]
    env:                Dict[str, Set[Tuple[int, int]]] # Contient les positions des buissons et des touffes
    images:             Dict[str, object]
    taille_image:       float
    historique:         List[Tuple[Mouton]]
    __slots__ = tuple(__annotations__)
    
    def __hash__(self):
        return hash(tuple(sorted(self.troupeau)))

    def __eq__(self, other):
        return sorted(self.troupeau) == sorted(other.troupeau)

    def __init__(self, gridfile: str,
                 grille_base=None,
                 grille_pos=(0, 0, cfg.largeur_fenetre, cfg.hauteur_fenetre),
                 test_mode=False, editeur=False):

        if not editeur:
            #print('Jeu reçu par l instance Plateau', gridfile)
            self.grid_parse(gridfile)

        else:
            self.grid_parselst(editeur)

        #print(self.env)
        if test_mode: return
        self.grille = Grille(self.nb_colonnes, self.nb_lignes,
                             grille_base=grille_base,
                             grille_pos=grille_pos)    
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
        self.historique = [tuple(deepcopy(self.troupeau))]

    def grid_parselst(self, editeur):
        self.troupeau = []
        self.env = {'buissons': set(), 'touffes': set()}
        self.nb_lignes = 0
        for lignes in editeur:
            self.nb_colonnes = 0
            for elem in lignes:
                pos = (self.nb_lignes, self.nb_colonnes)
                if elem == "B":
                    self.env['buissons'].add(pos)
                elif elem == 'G':
                    self.env['touffes'].add(pos)
                elif elem == "S":
                    self.troupeau.append(Mouton(*pos))
                self.nb_colonnes += 1
            self.nb_lignes += 1
        self.historique = [tuple(deepcopy(self.troupeau))]


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
                affiche_env_element(case, images[name])
        for m in self.troupeau:
            heureux = 'heureux' if m in self.env['touffes'] else 'mouton'
            case = self.grille.cases[m.y][m.x]
            affiche_env_element(case, images[heureux])   

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

    def deplace_moutons(self, direction: str, historique=False):
        if historique:
            self.historique.append(tuple(deepcopy(self.troupeau)))
        self.tri_moutons(direction)
        for mouton in self.troupeau:
            mouton.deplace(direction, self)

    def tri_moutons(self, direction):
        """
        Trie les moutons de sorte que le mouton le plus près
        du mur de la direction demandée soit le premier à être déplacé.
        """
        if direction in self.tri_moutons.DOWN_RIGHT:
            self.troupeau.sort(reverse=True)
        elif direction in self.tri_moutons.UP_LEFT:
            self.troupeau.sort(reverse=False)
    # Evite de recréer les sets à chaque appel
    tri_moutons.DOWN_RIGHT = {"Down", "Right"}
    tri_moutons.UP_LEFT = {"Up", "Left"}

    def reset(self):
        """
        Réinitialise à l'état initial de la map,
        et supprime l'historique
        """
        self.troupeau = list(deepcopy(self.historique[0]))
        del self.historique[1:]

    def undo(self):
        """
        Annule le dernier coup joué
        """
        if len(self.historique) >= 2:
            self.troupeau = list(self.historique.pop())
        
    def isGagne(self):
        occupe = 0
        for mouton in self.troupeau:
            if mouton in self.env['touffes']:
                occupe += 1
            if occupe == len(self.env['touffes']):
                return True
        return False

    def troupeau_savewrite(self, position_save):
        for mouton in self.troupeau:
            pos = position_save.pop()
            mouton.y = pos[0]
            mouton.x = pos[1]

    def historique_savewrite(self, historique_save):
        for temps in historique_save:
            for i in range(len(self.troupeau)):
                self.troupeau[i].x = temps[i][1]
                self.troupeau[i].y = temps[i][0]

            self.historique.append(tuple(deepcopy(self.troupeau)))
        self.undo()
