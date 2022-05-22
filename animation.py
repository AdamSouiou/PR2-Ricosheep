import fltk
import random
import cfg
from dataclasses import dataclass
from PIL import Image, ImageTk
from os import path
from typing import List, Optional

@dataclass
class FallingSheep:
    x: float
    y: float
    Sheep: object
    angle: int
    speed: float
    height: float

def initialisation(number: int):
    """
    Initialise les images et les objets FallingSheep contenant les moutons pour 
    l'animation du menu d'accueil selon le nombre "number, et renvoie
    la liste contenant tous les objets FallingSheep 
    """
    liste = []
    
    img1 = Image.open(path.join('media', 'images', 'chute1.png'))
    img2 = Image.open(path.join('media', 'images', 'chute2.png'))
    
    for _ in range(number+1):

        proportion = random.randint(1, 7)
        imagechute = (img1.copy()
                      if bool(random.getrandbits(1)) else
                      img2.copy())
        
        imagechute = resize(imagechute, 24, proportion)

        liste.append(
            FallingSheep(
                x= random.randint(0, cfg.largeur_fenetre),
                y=random.randint(int(-cfg.hauteur_fenetre*2), 0),
                Sheep=imagechute,
                speed=proportion,
                angle=random.randint(-60, 60),
                height=imagechute.height
            )
        )
        imagechute = imagechute.rotate(
            liste[-1].angle, expand=True, resample=Image.BICUBIC)
        liste[-1].height = imagechute.height
        liste[-1].Sheep = ImageTk.PhotoImage(imagechute)

    liste.sort(key=lambda elem: elem.speed)
    return liste

def resize(image: Image, taille: int, proportion: int = 1):
    """
    Redimensionne l'image donné selon la taille et la proportion
    """
    (width, height) = (image.width // taille * proportion,
                       image.height // taille * proportion)
    return image.resize((width, height), resample=Image.NEAREST)

def chute(elem: FallingSheep):
    """
    Fait "tombé" l'élément selon sa vitesse, sa taille et la taille de l'écran
    """
    elem.y += elem.speed
    elem.y = elem.y % (cfg.hauteur_fenetre + elem.height)

def dessiner(liste: List[FallingSheep]):
    """
    Dessine tous les éléments de la liste de FallingSheep
    """
    for elem in liste:
        fltk.afficher_image(elem.x, elem.y, elem.Sheep, ancrage='s')
        chute(elem)
