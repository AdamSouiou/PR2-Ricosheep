class Mouton:
    x: int
    y: int
    __slots__ = tuple(__annotations__)

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
    def __repr__(self):
        return f'(y={self.y}, x={self.x})'
    """def __gt__(self, other):
        if type(other) == tuple:
            return (self.y, self.x) > other
        return (self.y, self.x) > (other.y, other.x)
    def __iter__(self):
        return iter((self.y, self.x))
    """

    def __init__(self, y: int, x: int):
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