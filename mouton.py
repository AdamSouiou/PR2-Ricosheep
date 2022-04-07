from dataclasses import dataclass
from typing import List, Tuple
from plateau import Case

import graphiques


class Mouton:
    x: int
    y: int
    img_neutre: object
    img_herbe: object

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.img_neutre = "ntm"
        self.img_herbe = "ntp"
    
    def deplace_mouton(self, direction: str, plateau: List[List[Case]]):
        if direction == "Up":
            print("HAUT")

        if direction == "Left":
            print("GAUCHE")

        if direction == "Down":
            print("BAS")

        if direction == "Right":
            print("DROITE")
    
    def is_eating(self, plateau: List[List]):
        return plateau[self.y][self.x] == "G"

