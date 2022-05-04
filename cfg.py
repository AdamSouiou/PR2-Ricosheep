import json
import os


def maj():
    global largeur_fenetre, hauteur_fenetre, son, carte, carte_lst
    file = json.load(open('config.json'))

    largeur_fenetre = file['windows']['largeur_fenetre']
    hauteur_fenetre = file['windows']['hauteur_fenetre']
    son = file['son']
    carte = os.path.join("maps", file['carte'][0], file['carte'][1])
    carte_lst = file['carte']

def toggle_sound():
    with open("config.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data['son'] = son

    with open("config.json", "w+") as jsonFile:
        jsonFile.write(json.dumps(data, indent=4))
    

maj()