import fltk
from typing import List

def map_parse(file: str):
    plateau, moutons = [], []
    with open(file) as f:
        lines = f.readlines()
    for line in lines:
        row = []
        for char in line:
            if char in ('B', 'G'):
                row.append(char)
            elif char == 'S':
                moutons.append((len(plateau), len(row)))
            elif char in ('S', '_'):
                row.append(None)
        plateau.append(row)
    return plateau, moutons




print(map_parse('maps/square/map1.txt'))