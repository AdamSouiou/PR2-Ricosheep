from typing import List, Tuple


class Mouton:

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