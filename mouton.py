"""
Projet 2 : Ricosheep

Amal ABDALLAH
Nicolas SEBAN
Adam SOUIOU
"""

import operator
from dataclasses import dataclass


axes = {'Up': 'y', 'Down': 'y',
        'Left': 'x', 'Right': 'x'}
coeff_axe = {'Up': -1, 'Down': 1,
             'Left': -1, 'Right': 1}
axes_cases = {'Up': 'centre_y', 'Down': 'centre_y',
              'Left': 'centre_x', 'Right': 'centre_x'}


@dataclass
class Vitesse:
    x: float
    y: float


class Mouton:
    x: int
    y: int
    centre_x: float
    centre_y: float
    vitesse: Vitesse
    en_deplacement: bool
    __slots__ = tuple(__annotations__)

    def __hash__(self):
        return hash((self.y, self.x))

    def __eq__(self, other):
        if type(other) is tuple:
            return (self.y, self.x) == other
        return (self.y, self.x) == (other.y, other.x)

    def __ne__(self, other):
        if type(other) is tuple:
            return (self.y, self.x) != other
        return (self.y, self.x) != (other.y, other.x)

    def __lt__(self, other):
        if type(other) is tuple:
            return (self.y, self.x) < other
        return (self.y, self.x) < (other.y, other.x)

    def __repr__(self):
        return f'(y={self.y}, x={self.x})'

    def __init__(self, y: int, x: int):
        self.x = x
        self.y = y
        self.vitesse = Vitesse(0, 0)
        self.en_deplacement = False

    def repositionnement(self, cases):
        """
        Repositionne le mouton sur le centre de la case.
        """
        case = cases[self.y][self.x]
        self.centre_x = case.centre_x
        self.centre_y = case.centre_y
        self.vitesse.x = 0
        self.vitesse.y = 0
        self.en_deplacement = False

    def deplace(self, direction: str, plateau):
        """
        Déplace le mouton jusqu'a ce qu'il rencontre un obstacle
        """
        pos_initiale = (self.y, self.x)
        if direction == "Up":
            while plateau.isPositionValid(self.x, self.y-1):
                self.y -= 1

        elif direction == "Down":
            while plateau.isPositionValid(self.x, self.y+1):
                self.y += 1

        elif direction == "Left":
            while plateau.isPositionValid(self.x-1, self.y):
                self.x -= 1

        elif direction == "Right":
            while plateau.isPositionValid(self.x+1, self.y):
                self.x += 1

        self.en_deplacement = self != pos_initiale

    def deplace_vitesse(self, mouton_initial, plateau, direction):
        """
        Détermine la vitesse du mouton lors du déplacement animé
        pour satisfaire la contrainte de durée imposée par le
        plateau
        """
        if self.en_deplacement:
            distance = abs(
                getattr(self, axes[direction])
                - getattr(mouton_initial, axes[direction])
            ) * plateau.grille.largeur_case

            setattr(
                self.vitesse, axes[direction],
                coeff_axe[direction] * (distance / plateau.duree_anime)
            )

    def outOfBound(self, direction, cases, dt):
        """
        Vérifie si le mouton n'a pas dépassé sa case d'arrivée.
        """
        if direction in self.outOfBound.LEFT_UP:
            comparateur = operator.le
        elif direction in self.outOfBound.RIGHT_DOWN:
            comparateur = operator.ge

        return comparateur(
            getattr(
                self,
                axes_cases[direction]) + dt * getattr(self.vitesse,
                                                      axes[direction]),
            getattr(cases[self.y][self.x], axes_cases[direction])
        )

    outOfBound.LEFT_UP = {'Left', 'Up'}
    outOfBound.RIGHT_DOWN = {'Right', 'Down'}
