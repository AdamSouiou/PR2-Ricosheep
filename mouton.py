from typing import List, Tuple


class Mouton:
    __slots__ = ['x', 'y']
    def __hash__(self):
        return hash((self.y, self.x))
    def __eq__(self, other):
        if type(other) == tuple:
            return (self.y, self.x) == other
        return (self.y, self.x) == (other.y, other.x)
    def __lt__(self, other):
        if type(other) == tuple:
            return (self.y, self.x) < other
        return (self.y, self.x) < (other.y, other.x)
    def __gt__(self, other):
        if type(other) == tuple:
            return (self.y, self.x) > other
        return (self.y, self.x) > (other.y, other.x)
    def __iter__(self):
        return iter((self.y, self.x))

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        #self.ax_image 
        #self.bx_image

    def deplace(self, direction: str, plateau):
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