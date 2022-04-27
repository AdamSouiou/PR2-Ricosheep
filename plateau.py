from typing import List, Tuple, Dict, Set
from pprint import pprint
from mouton import Mouton
from graphiques import affiche_case
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
    last_direction:     str
    nb_places:          int
    anime:              bool
    vitesse:            float
    __slots__ = tuple(__annotations__)
    
    def __hash__(self):
        return hash(tuple(sorted(self.troupeau)))

    def __eq__(self, other):
        return sorted(self.troupeau) == sorted(other.troupeau)

    def __init__(self, gridfile: str, anime=False,
                 grille_base=None,
                 grille_pos=(0, 0, cfg.largeur_fenetre, cfg.hauteur_fenetre),
                 test_mode=False):
        print("Jeu reçu par l'instance Plateau", gridfile)
        self.grid_parse(gridfile)
        self.anime = anime
        self.vitesse = 10
        self.grille = Grille(self.nb_colonnes, self.nb_lignes,
                             grille_base=grille_base,
                             grille_pos=grille_pos)
        if anime: self.init_pos_mouton()
        self.taille_image = self.grille.largeur_case * 0.8
        self.last_direction = None
        self.nb_places = 0
    
        if test_mode: return
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
    
    def draw(self):
        self.grille.draw()
        for name, elements in self.env.items():
            for y,x in elements:
                affiche_case(x, y, self.grille, images[name])
        if self.anime:
            self.draw_moutons_anime()
        else:
            self.draw_moutons_simple()
    
    isHeureux = lambda self, mouton: ('heureux' if mouton in self.env['touffes']
                                      else 'mouton')
    affiche_mouton = lambda self, m: affiche_case(
        m.x, m.y, self.grille, images[self.isHeureux(m)]
    )
    
    def draw_moutons_simple(self):
        for m in self.troupeau:
                self.affiche_mouton(m)
    
    def init_pos_mouton(self):
        for mouton in self.troupeau:
            mouton.centre_x = self.grille.cases[mouton.y][mouton.x].centre_x
            mouton.centre_y = self.grille.cases[mouton.y][mouton.x].centre_y

    def draw_moutons_anime(self):
        fini = 0
        for mouton in self.troupeau:
            if not mouton.en_deplacement:
                self.affiche_mouton(mouton)
                fini += 1
                continue
            if self.last_direction is not None:
                if not mouton.isPlace(self.last_direction, self.grille.cases):
                    mouton.centre_x += mouton.vitesse.x
                    mouton.centre_y += mouton.vitesse.y
                else:
                    print("Salut, je m'arrête!")
                    mouton.vitesse.x = 0
                    mouton.vitesse.y = 0
                    mouton.en_deplacement = False
                    fini += 1
                
                fltk.afficher_image(
                    mouton.centre_x, mouton.centre_y,
                    image=images['mouton'], ancrage='center'
                )
        if fini == len(self.troupeau) and self.last_direction is not None:
            self.last_direction = None
            self.init_pos_mouton()

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

    def deplace_moutons(self, direction: str, solveur=False):
        # Evite le cas où le joueur appuie pendant le déplacement
        vitesse = 0
        if not solveur:
            if self.last_direction is not None: return
            if self.anime:
                self.last_direction = direction
                vitesse = self.vitesse
            self.historique.append(tuple(deepcopy(self.troupeau)))

        self.tri_moutons(direction)
        for mouton in self.troupeau:
            mouton.deplace(direction, self, vitesse)
        
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
        if self.anime: self.init_pos_mouton()

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