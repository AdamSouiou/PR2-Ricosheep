import json
import os


def maj():
    global largeur_fenetre, hauteur_fenetre, son, carte
    file = json.load(open('config.json'))

    largeur_fenetre = file['windows']['largeur_fenetre']
    hauteur_fenetre = file['windows']['hauteur_fenetre']
    son = file['son']
    carte = os.path.join("maps", file['carte'][0], file['carte'][1])

maj()