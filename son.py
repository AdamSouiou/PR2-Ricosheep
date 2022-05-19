import random
import os 
import cfg

try:
    import pygame
    pygame_available = True

except:
    pygame_available = False
    cfg.son = False
    print("Veuillez installez pygame pour accéder à l'expérience sonore.")

def initialisation():
    if pygame_available:
        pygame.init()
        global menu_accept, menu_bleep, sheep
        menu_accept = pygame.mixer.Sound(os.path.join('son', 'MenuAccept.wav'))
        menu_bleep = pygame.mixer.Sound(os.path.join('son', 'MenuBleep.wav'))
        sheep1 = pygame.mixer.Sound(os.path.join('son', 'sheep1.wav'))
        sheep2 = pygame.mixer.Sound(os.path.join('son', 'sheep2.wav'))
        sheep3 = pygame.mixer.Sound(os.path.join('son', 'sheep3.wav'))
        sheep4 = pygame.mixer.Sound(os.path.join('son', 'sheep4.wav'))
        pygame.mixer.Sound.set_volume(menu_accept, 0.7)
        pygame.mixer.Sound.set_volume(menu_bleep, 0.7)
        pygame.mixer.Sound.set_volume(sheep1, 0.7)
        pygame.mixer.Sound.set_volume(sheep2, 0.7)
        pygame.mixer.Sound.set_volume(sheep3, 0.7)
        pygame.mixer.Sound.set_volume(sheep4, 0.7)
        sheep = [sheep1, sheep2, sheep3, sheep4]

def sound(type):
    if pygame_available and cfg.son:
        if type == "MenuOk":
            menu_accept.play()
        if type == "Menubeep":
            menu_bleep.play()
        if type == "Sheep":
            beeeh = random.randint(1,10)
            if beeeh == 10:
                sheep[3].play()
                return
            beeeh = random.randint(0,2)
            sheep[beeeh].play()

def toggle_sound():
    if pygame_available:
        pygame.mixer.music.stop()
        cfg.toggle_sound_anim('sound')
        if cfg.son:
            song('Wait')
        

def song(name):
    if pygame_available and cfg.son:
        pygame.mixer.music.load(os.path.join('son', f'{name}.mp3'))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.8)

