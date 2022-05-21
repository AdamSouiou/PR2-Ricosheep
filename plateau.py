from typing import List, Tuple, Dict, Set, Union, Iterable, Sequence, NamedTuple
from os import PathLike
from time import time
from pprint import pprint
from mouton import Mouton
from graphiques import affiche_case, box_image
from grille import Grille
from copy import copy, deepcopy
import fltk
import cfg


class FichierInvalide(Exception):
    pass


class Plateau:
    # Utiliser __slots__ pour les gains de mémoire...
    # Il faudrait que troupeau soit un set...

    grille:             Grille
    nb_colonnes:        int
    nb_lignes:          int
    troupeau:           List[Mouton]
    env:                Dict[str, Set[Tuple[int, int]]]  # Contient les positions des buissons et des touffes
    images:             Dict[str, object]
    taille_image:       float
    historique:         List[Tuple[Mouton]]
    last_direction:     str
    nb_places:          int
    anime:              bool
    duree_anime:        float
    __slots__ = tuple(__annotations__)

    def __hash__(self):
        return hash(tuple(sorted(self.troupeau)))

    def __eq__(self, other):
        return sorted(self.troupeau) == sorted(other.troupeau)

    def __init__(self,
                 gridfile: Union[Sequence[Sequence[str]], PathLike, NamedTuple],
                 duree_anime=0.15,
                 grille_base=None,
                 grille_pos=(0, 0, cfg.largeur_fenetre, cfg.hauteur_fenetre),
                 parsed_data=[],
                 test_mode=False):

        #print('Jeu reçu par l instance Plateau', gridfile)
        if parsed_data:
            self.parse_tuple(*parsed_data)
        else:
            self.grid_parse(gridfile)

        self.duree_anime = duree_anime
        self.anime = False
        self.last_direction = None
        self.nb_places = 0
        if not test_mode:
            self.gen_grille(duree_anime, grille_base, grille_pos)

    def gen_grille(self,
                   duree_anime=0,
                   grille_base=None,
                   grille_pos=(0, 0, cfg.largeur_fenetre, cfg.hauteur_fenetre)):
        self.anime = bool(duree_anime)
        self.grille = Grille(self.nb_colonnes, self.nb_lignes,
                             grille_base=grille_base,
                             grille_pos=grille_pos)
        self.reset()
        self.reposition_moutons()
        self.taille_image = self.grille.largeur_case * 0.8

        global images
        images = {
            "buissons": box_image('media/images/bush.png', (self.taille_image,)),
            "touffes": box_image('media/images/grass.png', (self.taille_image,)),
            "mouton": box_image('media/images/sheep.png', (self.taille_image,)),
            "heureux": box_image('media/images/sheep_grass.png', (self.taille_image,))
        }

    def parse_tuple(self,
                    troupeau: Iterable[tuple],
                    buissons: Iterable[tuple],
                    herbes: Iterable[tuple],
                    lignes: int, colonnes: int):
        self.env = {'buissons': buissons, 'touffes': herbes}
        self.troupeau = [Mouton(m[0], m[1]) for m in troupeau]
        self.nb_lignes = lignes
        self.nb_colonnes = colonnes
        self.historique = [tuple(deepcopy(self.troupeau))]

    def grid_parse(self, data: Union[List[List[str]], PathLike]):
        it = open(data, 'r') if type(data) is str else data
        self.troupeau = []
        self.env = {'buissons': set(), 'touffes': set()}
        self.nb_lignes = 0
        len_first_line = 0
        for i, ligne in enumerate(it):
            self.nb_colonnes = 0
            for char in ligne:
                pos = (self.nb_lignes, self.nb_colonnes)
                if char == 'B':
                    self.env['buissons'].add(pos)
                elif char == 'G':
                    self.env['touffes'].add(pos)
                elif char == 'S':
                    self.troupeau.append(Mouton(*pos))
                elif char == '_':
                    pass
                elif char == '\n':
                    continue
                else:
                    raise FichierInvalide(
                        f"Le fichier contient un caractère non reconnu: {char}",
                        f"à la ligne {self.nb_lignes}, colonne {self.nb_colonnes}")
                self.nb_colonnes += 1
            if i == 0:
                len_first_line = self.nb_colonnes
            else:
                if self.nb_colonnes != len_first_line:
                    raise FichierInvalide(
                        "Les lignes n'ont pas tous la même longueur"
                    )
            self.nb_lignes += 1
        if self.nb_lignes == 0:
            raise FichierInvalide("Le fichier est vide !")
        self.historique = [tuple(deepcopy(self.troupeau))]
        if type(data) is str: it.close()

    def draw(self, start_time=0, dt=0):
        self.grille.draw()
        for name, elements in self.env.items():
            for y, x in elements:
                affiche_case(x, y, self.grille, images[name])
        if self.anime:
            self.draw_moutons_anime(start_time, dt)
        else:
            self.draw_moutons_simple()

    isHeureux = lambda self, mouton: ('heureux' if mouton in self.env['touffes']
                                      else 'mouton')

    affiche_mouton = lambda self, m: affiche_case(
        m.x, m.y, self.grille, images[self.isHeureux(m)]
    )

    def reposition_moutons(self):
        for mouton in self.troupeau:
            mouton.repositionnement(self.grille.cases)

    def draw_moutons_simple(self):
        for m in self.troupeau:
            self.affiche_mouton(m)

    def draw_moutons_anime(self, start_time=0, dt=0):
        fini = 0
        for mouton in self.troupeau:
            if not mouton.en_deplacement:
                self.affiche_mouton(mouton)
                fini += 1
                continue
            if self.last_direction is not None:
                if not mouton.outOfBound(self.last_direction, self.grille.cases, dt):
                    mouton.centre_x += mouton.vitesse.x * dt
                    mouton.centre_y += mouton.vitesse.y * dt
                else:
                    mouton.en_deplacement = False
                    fini += 1
                
                fltk.afficher_image(
                    mouton.centre_x, mouton.centre_y,
                    image=images['mouton'], ancrage='center'
                )
        if fini == len(self.troupeau) and self.last_direction is not None:
            self.last_direction = None
            self.reposition_moutons()
            #print(f'Temps du déplacement: {(time() - start_time - dt):.3f}s')


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
        return (0 <= y < self.nb_lignes
                and (0 <= x < self.nb_colonnes)
                and not (y, x) in self.env['buissons']
                and self.isNotPosMouton(x, y))

    def deplace_moutons(self, direction: str, solveur=False):
        """
        Déplace les moutons dans la direction demandée.
        Le booléen solveur est utilisé pour éviter de
        d'actualiser l'historique.
        Retourne si un déplacement devra être réalisé
        """
        deplacement = False
        if not solveur:
            self.historique.append(tuple(deepcopy(self.troupeau)))
            if self.anime:
                self.last_direction = direction

        self.tri_moutons(direction)
        for mouton in self.troupeau:
            if self.anime: mouton_initial = copy(mouton)
            mouton.deplace(direction, self)
            if self.anime:
                mouton.deplace_vitesse(mouton_initial, self, direction)
            if mouton.en_deplacement: deplacement = True
        
        return deplacement
                

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

    def clear_historique(self):
        del self.historique[1:]

    def reset(self):
        """
        Réinitialise à l'état initial de la map,
        et supprime l'historique
        """
        self.troupeau = list(deepcopy(self.historique[0]))
        self.clear_historique()
        self.reposition_moutons()

    def undo(self):
        """
        Annule le dernier coup joué
        """
        if len(self.historique) >= 2:
            self.troupeau = list(self.historique.pop())
        self.reposition_moutons()

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
