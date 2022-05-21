import fltk
import os
import json
from plateau import Plateau, FichierInvalide

DOSSIER = {
    "accueil.py", "animation.py", "bouton.py", "cfg.py",
    "config.json", "creation_niveaux.py", "editeur.py", "fltk.py",
    "graphiques.py", "grille.py", "mouton.py", "plateau.py",
    "randomizer.py", "README.md", "ricosheep.py", "sauvegarde.py",
    "savefile.json","selecteur.py","solveur.py", "son.py", "unit-tests.py"}

MEDIA = {
    'music': ['Otherside.mp3', 'Wait.mp3'], 
    'son':['MenuAccept.wav', 'MenuBleep.wav', 'sheep1.wav',
           'sheep2.wav', 'sheep3.wav', 'sheep4.wav'],
    'images':['bush.png', 'chute1.png', 'chute2.png', 'grass.png',
              'Illustration.png', 'Logo_ricosheep.png', 'sheep_grass.png', 'sheep.png',
              'icone.ico']
}

CHARACTER = {'B', 'G', 'S', '_', '\n'}

def files_check():
    files = os.listdir()
    for fichier in DOSSIER:
        if fichier not in files:
            if fichier == "config.json":
                create_configjson()
            elif fichier == "savefile.json":
                create_savefile()
            else:
                print(f"\nIl vous manque au moins {fichier}, veuillez réinstaller "
                      "Ricosheep pour résoudre ce problème.\n")
                return False
    return True

def media_check():
    dossier_utilisateur = os.listdir('media')
    for dossier in MEDIA:
        if dossier not in dossier_utilisateur:
            print(f"\nIl vous manque au moins le dossier {dossier}, "
                  "veuillez réinstaller Ricosheep pour résoudre ce problème.\n")
            return False
        fichier_utilisateur = os.listdir(os.path.join('media', dossier))
        for fichier in MEDIA[dossier]:
            if fichier not in fichier_utilisateur:
                print(f"\nIl vous manque au moins le fichier {fichier}, "
                      "veuillez réinstaller Ricosheep pour résoudre ce problème.\n")
                return False
    return True
        

def niveaux_check():
    global file, dos
    try: 
        dossier = os.listdir(os.path.join("maps"))
    except:
        print("\nVous n'avez même pas de dossier 'maps', "
              "veuillez suivre l'installation de Ricosheep pour "
              "profiter pleinement du jeu.\n")
        return False
    niveau = True
    if dossier != []:
        for sous_dos in dossier:
            dos = sous_dos
            test = os.listdir(os.path.join("maps", sous_dos))
            file = test[0]
            if file[-4:] == ".txt":
                try:
                    Plateau(os.path.join("maps", sous_dos, file),
                            test_mode=True)
                    return True
                except FichierInvalide:
                    niveau = False
    if niveau == False:
        print("\nVous n'avez aucun niveau dans le bon format, "
              "veuillez installer ne serait-ce que les niveaux fournis "
              "avec l'installation du jeu.\n")
    else:
        print("\nVous n'avez aucun niveau jouable, "
              "veuillez installer ne serait-ce que les niveaux fournis "
              "avec l'installation du jeu.\n")

    return False


def create_configjson():
    data = {}

    data['windows'] = {"largeur_fenetre":1000, "hauteur_fenetre":500}
    data['son'] = True
    data['animation'] = True
    data['carte'] = [dos, file]

    with open("config.json", "w+") as jsonFile:
        jsonFile.write(json.dumps(data, indent=4))


def create_savefile():
    data = {}

    data['carte'] = []
    data['historique'] = []
    data['position'] = []

    with open("savefile.json", "w+") as jsonFile:
        jsonFile.write(json.dumps(data))


def main():
    if fltk.PIL_AVAILABLE == False:
        print('\nVeuillez installer PIL pour pouvoir jouer au jeu.\n')
        exit()

    else:
        if not files_check() or not media_check() or not niveaux_check():
            exit()
