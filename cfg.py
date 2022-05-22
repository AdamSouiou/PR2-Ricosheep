import json
import os


def maj() -> None:
    """
    Créer des variables globales contenant les données de config.json
    """
    global largeur_fenetre, hauteur_fenetre, son, animation, carte, carte_lst
    file = json.load(open('config.json'))

    largeur_fenetre = file['windows']['largeur_fenetre']
    hauteur_fenetre = file['windows']['hauteur_fenetre']
    son = file['son']
    animation = file['animation']
    carte = os.path.join("maps", file['carte'][0], file['carte'][1])
    carte_lst = file['carte']

def toggle_sound_anim(option: str) -> None:
    """
    Change la variable de son ou de l'animation se l'option donné.
    """
    with open("config.json", "r") as jsonFile:
        data = json.load(jsonFile)

    if option == 'sound':
        data['son'] = son
    if option == 'animation':
        data['animation'] = animation

    with open("config.json", "w+") as jsonFile:
        jsonFile.write(json.dumps(data, indent=4))

maj()