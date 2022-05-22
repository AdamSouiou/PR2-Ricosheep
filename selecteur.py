"""
Projet 2 : Ricosheep

Amal ABDALLAH
Nicolas SEBAN
Adam SOUIOU
"""

import os
import json
from typing import Optional
from bouton import Boutons
from graphiques import close, background
import fltk
from plateau import Plateau, FichierInvalide
import son


def menu():
    split = 0
    directory = ""
    racine = os.listdir("maps")
    choix = None
    plateau = None
    boutons = init_boutons(split, directory)

    while True:
        try:
            fltk.efface_tout()
            background("#3f3e47")
            #boutons.grille.draw()
            boutons.dessiner_boutons()
            
            if plateau is not None: plateau.draw()
            
            ev = fltk.attend_ev()
            tev = fltk.type_ev(ev)
            click = boutons.nom_clic(ev)

            if tev == 'Quitte':
                close()
            elif tev == "Touche":
                touche = fltk.touche(ev)
                if touche == "Escape":
                    return

            elif tev == "ClicGauche":
                if click not in {None, "Valider", choix}:
                    son.sound('MenuBleep')
                    if click == "=>":
                        split += 1
                    elif click == "<=":
                        split -= 1

                    elif click == "\...":
                        directory = ""
                        split = 0
                    elif click in racine:
                        directory = click
                        split = 0

                    else:
                        choix = modif_json(directory, click)
                        try:
                            plateau = open_plateau(choix, boutons)
                        except FichierInvalide as e:
                            plateau = None
                            choix = None
                            print(e)
                    boutons = init_boutons(split, directory, choix)

                if click == "Valider":
                    son.sound('MenuAccept')
                    return

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()


def open_plateau(choix: str, boutons: Boutons) -> Plateau:
    """
    Créer un plateau selon la carte et la positionne à une zone spécifique de la grille des boutons.

    :param str choix: chemin vers un fichier de carte
    :param Boutons boutons: Boutons utilisé sur le menu
    :return Plateau: plateau de jeu fait avec la carte
    """
    if choix is not None:
        plateau = Plateau(
            os.path.join("maps", choix),
            grille_base=boutons.grille,
            grille_pos=(6, 3, 8, 6),
            duree_anime=0
        )
    else:
        plateau = None
    return plateau


def init_boutons(split: int = 0, directory: str = "", choix: Optional[str] = None) -> Boutons:
    """
    Initialise des boutons pour le menu selon le dossier, le sous-dossier et à quelle tranche où nous sommes dans le découpage.

    :param int split: Incrémentation dans le découpage par 5 dans la liste des sous-dossiers ou des cartes.
    :param str directory: Sous-dossier qu'on regarde.
    :param str choix: Chemin complet faire une carte contenu dans un des sous-dossier.
    :return Boutons: Boutons utilisé dans le menu.
    """

    dossiers = os.listdir(os.path.join("maps", directory))
    dossiers.sort()
    boutons = Boutons((10,10))

    if directory != "":
        boutons.cree_bouton_simple(5, 1, 8, 1, "\...", unifier_texte=False)

    if choix:
        boutons.cree_bouton_texte(1, 9, 8, 9, choix)

    if len(dossiers) <= 6:
        for i in range(len(dossiers)):
            boutons.cree_bouton_simple(1, 1+i, 4, 1+i, dossiers[i])    

    else:
        if split > 0:
            dos = dossiers[5*split:5*(split+1)]
            boutons.cree_bouton_simple(1, 6, 2, 6, "<=")
            if len(dossiers) > 5*(split+1):
                boutons.cree_bouton_simple(3, 6, 4, 6, "=>")
        else:
            dos = dossiers[:5]
            boutons.cree_bouton_simple(3, 6, 4, 6, "=>")
        for i in range(len(dos)):
            boutons.cree_bouton_simple(1, 1+i, 4, 1+i, dos[i])

    boutons.cree_bouton_simple(1, 8, 4, 8, "Valider", arrondi=0.75, unifier_texte=False)

    boutons.init()
    return boutons

def modif_json(directory: str, file: str) -> str:
    """
    Modifie le fichier config.json pour changer la variable carte pour contenir le sous-dossier et le fichier du niveau,
    et renvoie le chemin d'accès au fichier du niveau

    :param str directory: Sous-dossier cotenant le fichier du niveau
    :param str file: Fichier du niveau.
    :return str: Chemin d'accès vers le fichier.
    """

    with open("config.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data['carte'][0] = directory
    data['carte'][1] = file

    with open("config.json", "w+") as jsonFile:
        jsonFile.write(json.dumps(data, indent=4))

    return os.path.join(directory, file)
