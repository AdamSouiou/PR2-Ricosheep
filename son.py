import random
import os 
import cfg

MEDIA = {
    "music": ["Otherside.mp3", "Wait.mp3"], 
    "son":["MenuAccept.wav", "MenuBleep.wav", "sheep1.wav",
           "sheep2.wav", "sheep3.wav", "sheep4.wav"],
}

try:
    import pygame
    PYGAME_AVAILABLE = True
    liste_son = {}

except:
    PYGAME_AVAILABLE = False
    cfg.son = False
    print("Veuillez installer pygame pour accéder à l'expérience sonore.")

def initialisation() -> None:
    """
    Initialise tous les effets sonores ainsi que leurs volumes.
    """
    global liste_son
    if PYGAME_AVAILABLE:
        pygame.init()
        liste_son = {}
        for son in MEDIA['son']:
            liste_son[son[:-4]] = pygame.mixer.Sound(os.path.join('media', 'son', son))

        for son in liste_son:
            pygame.mixer.Sound.set_volume(liste_son[son], 0.7)
        

def sound(type: str) -> None:
    """
    Fais un bruitage sonore selon le type de son demandé en entrée.

    :param str: Nom du bruitage joué
    """
    if PYGAME_AVAILABLE and cfg.son:
        if type == "Sheep":
            beeeh = random.randint(1,10)
            if beeeh == 10:
                liste_son['sheep4'].play()
                return
            beeeh = random.randint(0,2)
            liste_son[f'sheep{beeeh+1}'].play()
        else:
            liste_son[type].play()

def toggle_sound() -> None:
    """
    Désactive la musique et les sons ou les réactive en changeant l'état de "sound"
    """
    if PYGAME_AVAILABLE:
        pygame.mixer.music.stop()
        cfg.toggle_sound_anim('sound')
        if cfg.son:
            song('Wait')
        

def song(name: str) -> None:
    """
    Prends en entrée le nom du fichier mp3 pour le jouer.

    :param str: nom du fichier à jouer.
    """
    if PYGAME_AVAILABLE and cfg.son:
        pygame.mixer.music.load(os.path.join('media','music', f'{name}.mp3'))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.8)
