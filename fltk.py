import subprocess
import sys
import tkinter as tk
import tkinter.simpledialog
from typing import Union, Tuple, Optional, Literal, List
from tkinter import Entry
from collections import deque
from os import system, PathLike
from time import time, sleep
from tkinter.font import Font

try:
    from PIL import Image, ImageTk
    print("Bibliothèque PIL chargée.", file=sys.stderr)
    PIL_AVAILABLE = True

except ImportError:
    PIL_AVAILABLE = False

__all__ = [
    # gestion de fenêtre
    'cree_fenetre',
    'ferme_fenetre',
    'mise_a_jour',
    # dessin
    'ligne',
    'fleche',
    'polygone',
    'rectangle',
    'cercle',
    'point',
    # Images
    'afficher_image',
    'taille_image',
    'redimensionner_image',
    # Texte
    'texte',
    'taille_texte',
    # effacer
    'efface_tout',
    'efface',
    # utilitaires
    'attente',
    'capture_ecran',
    'touche_pressee',
    'abscisse_souris',
    'ordonnee_souris',
    # événements
    'donne_ev',
    'attend_ev',
    'attend_clic_gauche',
    'attend_fermeture',
    'type_ev',
    'abscisse',
    'ordonnee',
    'touche'
]


class CustomCanvas:
    """
    Classe qui encapsule tous les objets tkinter nécessaires à la création
    d'un canevas.
    """

    _on_osx = sys.platform.startswith("darwin")
    _on_win = sys.platform.startswith("win32")

    _ev_mapping = {
        'ClicGauche': '<Button-1>',
        'ClicMilieu': '<Button-2>',
        'ClicDroit': '<Button-2>' if _on_osx else '<Button-3>',
        'Deplacement': '<Motion>',
        'Touche': '<Key>'
    }

    _default_ev = ['ClicGauche', 'ClicDroit', 'Touche']

    def __init__(self, width, height, title='tk',
                 refresh_rate=60, events=None, icone=None):
        # width and height of the canvas
        self.width = width
        self.height = height
        self.interval = 1/refresh_rate

        # root Tk object
        self.root = tk.Tk()
        self.root.title(title)
        if icone:
            self.root.iconphoto(True, ImageTk.PhotoImage(file=icone))
            if self._on_win:
                import ctypes
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    title
                )

        # canvas attached to the root object
        self.canvas = tk.Canvas(self.root, width=width,
                                height=height, highlightthickness=0)

        # adding the canvas to the root window and giving it focus
        self.canvas.pack()
        self.canvas.focus_set()

        # binding events
        self.ev_queue = deque()
        self.pressed_keys = set()
        self.events = CustomCanvas._default_ev if events is None else events
        self.bind_events()

        # marque
        self.tailleMarque = 5

        # update for the first time
        self.last_update = time()
        self.root.update()

        if CustomCanvas._on_osx:
            system('''/usr/bin/osascript -e 'tell app "Finder" \
                   to set frontmost of process "Python" to true' ''')

    def update(self):
        t = time()
        self.root.update()
        sleep(max(0., self.interval - (t - self.last_update)))
        self.last_update = time()

    def bind_events(self):
        self.root.protocol("WM_DELETE_WINDOW", self.event_quit)
        self.canvas.bind('<KeyPress>', self.register_key)
        self.canvas.bind('<KeyRelease>', self.release_key)
        for name in self.events:
            self.bind_event(name)

    def register_key(self, ev):
        self.pressed_keys.add(ev.keysym)

    def release_key(self, ev):
        if ev.keysym in self.pressed_keys:
            self.pressed_keys.remove(ev.keysym)

    def event_quit(self):
        self.ev_queue.append(("Quitte", ""))

    def bind_event(self, name):
        e_type = CustomCanvas._ev_mapping.get(name, name)

        def handler(event, _name=name):
            self.ev_queue.append((_name, event))
        self.canvas.bind(e_type, handler, '+')

    def unbind_event(self, name):
        e_type = CustomCanvas._ev_mapping.get(name, name)
        self.canvas.unbind(e_type)


__canevas = None
__img = dict()


# ############################################################################
# Exceptions
#############################################################################


class TypeEvenementNonValide(Exception):
    pass


class FenetreNonCree(Exception):
    pass


class FenetreDejaCree(Exception):
    pass


class PILError(Exception):
    pass

# Vous êtes viré, c'est scandaleux


#############################################################################
# Initialisation, mise à jour et fermeture
#############################################################################


def cree_fenetre(largeur: int, hauteur: int,
                 titre: str = 'tk', frequence: int = 60,
                 icone: Optional[PathLike] = None) -> None:
    """
    Crée une fenêtre avec un titre et une icône, de dimensions
    ``largeur`` x ``hauteur`` pixels, et avec une frequence de
    rafraîchissement de 100 images par secondes par défaut.
    :rtype:
    """
    global __canevas
    if __canevas is not None:
        raise FenetreDejaCree(
            'La fenêtre a déjà été crée avec la fonction "cree_fenetre".')
    __canevas = CustomCanvas(largeur, hauteur, titre, frequence, icone=icone)


def taille_fenetre() -> Tuple[int, int]:
    """
    Retourne la taille actuelle de la fenêtre
    """
    return (__canevas.root.winfo_width(),
            __canevas.root.winfo_height())


def ferme_fenetre() -> None:
    """
    Détruit la fenêtre.
    """
    global __canevas
    if __canevas is None:
        raise FenetreNonCree(
            "La fenêtre n'a pas été crée avec la fonction \"cree_fenetre\".")
    __canevas.root.destroy()
    __canevas = None


def mise_a_jour() -> None:
    """
    Met à jour la fenêtre. Les dessins ne sont affichés qu'après
    l'appel à  cette fonction.
    """
    if __canevas is None:
        raise FenetreNonCree(
            "La fenêtre n'a pas été crée avec la fonction \"cree_fenetre\".")
    __canevas.update()


#############################################################################
# Fonctions de dessin
#############################################################################


# Formes géométriques

def ligne(ax: float, ay: float, bx: float, by: float,
          couleur: str = 'black', epaisseur: float = 1, tag=''):
    """
    Trace un segment reliant le point ``(ax, ay)`` au point ``(bx, by)``.

    :param float ax: abscisse du premier point
    :param float ay: ordonnée du premier point
    :param float bx: abscisse du second point
    :param float by: ordonnée du second point
    :param str couleur: couleur de trait (défaut 'black')
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    return __canevas.canvas.create_line(
        ax, ay, bx, by,
        fill=couleur,
        width=epaisseur,
        tag=tag)


def fleche(ax: float, ay: float, bx: float, by: float,
           couleur: str = 'black', epaisseur: float = 1, tag=''):
    """
    Trace une flèche du point ``(ax, ay)`` au point ``(bx, by)``.

    :param float ax: abscisse du premier point
    :param float ay: ordonnée du premier point
    :param float bx: abscisse du second point
    :param float by: ordonnée du second point
    :param str couleur: couleur de trait (défaut 'black')
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    x, y = (bx - ax, by - ay)
    n = (x**2 + y**2)**.5
    x, y = x/n, y/n
    points = [bx, by, bx-x*5-2*y, by-5*y+2*x, bx-x*5+2*y, by-5*y-2*x]
    return __canevas.canvas.create_polygon(
        points,
        fill=couleur,
        outline=couleur,
        width=epaisseur,
        tag=tag)


def polygone(points: List[Tuple[float, float]],
             couleur: str = 'black',
             remplissage: str = '',
             remplissage_actif: str = '',
             epaisseur: float = 1, tag=''):
    """
    Trace un polygone dont la liste de points est fournie.

    :param list points: liste de couples (abscisse, ordonnee) de points
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    return __canevas.canvas.create_polygon(
        points,
        fill=remplissage,
        activefill=remplissage_actif,
        outline=couleur,
        width=epaisseur,
        tag=tag)


def rectangle(ax: float, ay: float, bx: float, by: float,
              couleur: str = 'black',
              remplissage: str = '',
              remplissage_actif: str = '',
              epaisseur: float = 1, tag=''):
    """
    Trace un rectangle noir ayant les point ``(ax, ay)`` et ``(bx, by)``
    comme coins opposés.

    :param float ax: abscisse du premier coin
    :param float ay: ordonnée du premier coin
    :param float bx: abscisse du second coin
    :param float by: ordonnée du second coin
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param str remplissage_actif: couleur lors du survol (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    return __canevas.canvas.create_rectangle(
        ax, ay, bx, by,
        outline=couleur,
        fill=remplissage,
        activefill=remplissage_actif,
        width=epaisseur,
        tag=tag)


def cercle(x: float, y: float, r: float,
           couleur: str = 'black',
           remplissage: str = '',
           epaisseur: float = 1, tag=''):
    """
    Trace un cercle de centre ``(x, y)`` et de rayon ``r`` en noir.

    :param float x: abscisse du centre
    :param float y: ordonnée du centre
    :param float r: rayon
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    return __canevas.canvas.create_oval(
        x - r, y - r, x + r, y + r,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tag=tag)


def arc(x: float, y: float, r: float,
        ouverture: float = 90, depart: float = 0,
        couleur: str = 'black', remplissage: str = '',
        epaisseur: float = 1, tag=''):
    """
    Trace un arc de cercle de centre ``(x, y)``, de rayon ``r`` et
    d'angle d'ouverture ``ouverture`` (défaut : 90 degrés, dans le sens
    contraire des aiguilles d'une montre) depuis l'angle initial ``depart``
    (défaut : direction 'est').

    :param float x: abscisse du centre
    :param float y: ordonnée du centre
    :param float r: rayon
    :param float ouverture: abscisse du centre
    :param float depart: ordonnée du centre
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    return __canevas.canvas.create_arc(
        x - r, y - r, x + r, y + r,
        extent=ouverture,
        start=depart,
        style=tk.ARC,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tag=tag)


def point(x: float, y: float,
          couleur: str = 'black', epaisseur: float = 1,
          tag=''):
    """
    Trace un point aux coordonnées ``(x, y)`` en noir.

    :param float x: abscisse
    :param float y: ordonnée
    :param str couleur: couleur du point (défaut 'black')
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    return cercle(x, y, epaisseur,
                  couleur=couleur,
                  remplissage=couleur,
                  tag=tag)


# Image

def afficher_image(x: float, y: float,
                   image: Union[PathLike, Image.Image],
                   ancrage: str = 'center', tag='') -> Image:
    """
    Affiche l'image avec ``(x, y)`` comme centre. Les
    valeurs possibles du point d'ancrage sont ``'center'``, ``'nw'``, etc.

    :param float x: abscisse du point d'ancrage
    :param float y: ordonnée du point d'ancrage
    :param image: nom du fichier contenant l'image, ou un objet image
    :param ancrage: position du point d'ancrage par rapport à l'image
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    if type(image) == str:
        if PIL_AVAILABLE:
            with Image.open(image) as img:
                tkimage = ImageTk.PhotoImage(img)
        else:
            tkimage = tk.PhotoImage(file=image)
    else:
        tkimage = image

    img_object = __canevas.canvas.create_image(
        x, y, anchor=ancrage, image=tkimage, tag=tag
    )
    __img[img_object] = tkimage

    return img_object


def taille_image(fichier: PathLike) -> Tuple[int, int]:
    """
    Retourne un tuple représentant la largeur et la hauteur
    de l'image.

    :param str fichier: Nom du fichier image
    """
    if PIL_AVAILABLE:
        with Image.open(fichier) as img:
            return img.size

    raise PILError("Cette fonction est disponible \
                   uniquement si PIL est présent")
    return None


def redimensionner_image(fichier: PathLike, coeff: float, reechantillonage=None):
    """
    Ouvre une image et la redimensionne avec un coefficient multiplicateur,
    il est également possible d'appliquer un filtre de réchantillonage pour
    améliorer le rendu du redimensionnement:
    Au plus proche: ``0``
    Lanczoz: ``1``
    Bilinéaire: ``2``
    Bicubique: ``3``
    Box: ``4``
    Hamming: ``5``
    :param fichier: Fichier de l'image à redimensioner
    :param float coeff: Coefficient de redimensionnement
    :param int reechantillonage: {0, 1, 2, 3, 4, 5} Algorithme à utiliser pour
    améliorer le rendu, ``None``pour aucun.
    :return: Objet image
    """

    if PIL_AVAILABLE:
        with Image.open(fichier) as img:
            taille = img.size
            taille_coeff = (int(taille[0]*coeff), int(taille[1]*coeff))
            return ImageTk.PhotoImage(
                img.resize(taille_coeff, reechantillonage)
            )
    else:
        PILError()
        return None


def texte(x: float, y: float, chaine: str,
          couleur: str = 'black',
          ancrage: Literal[
              'nw', 'n', 'ne', 'w', 'center', 'e', 'sw', 's', 'se'
          ] = 'nw',
          police: str = 'Helvetica', taille: int = 24, tag=''):
    """
    Affiche la chaîne ``chaine`` avec ``(x, y)`` comme point d'ancrage (par
    défaut le coin supérieur gauche).

    :param float x: abscisse du point d'ancrage
    :param float y: ordonnée du point d'ancrage
    :param str chaine: texte à afficher
    :param str couleur: couleur de trait (défaut 'black')
    :param ancrage: position du point d'ancrage (défaut 'nw')
    :param police: police de caractères (défaut : `Helvetica`)
    :param taille: taille de police (défaut 24)
    :param tag: étiquette d'objet (défaut : pas d'étiquette
    :return: identificateur d'objet
    """

    return __canevas.canvas.create_text(
        x, y,
        text=chaine, font=(police, taille), tag=tag,
        fill=couleur, anchor=ancrage, state='disabled')


def taille_texte(chaine: str, police: str = 'Helvetica', taille: int = 24):
    """
    Donne la largeur et la hauteur en pixel nécessaires pour afficher
    ``chaine`` dans la police et la taille données.

    :param str chaine: chaîne à mesurer
    :param police: police de caractères (défaut : `Helvetica`)
    :param taille: taille de police (défaut 24)
    :return: couple (w, h) constitué de la largeur et la hauteur de la chaîne
        en pixels (int), dans la police et la taille données.
    """
    font = Font(family=police, size=taille)
    return font.measure(chaine), font.metrics("linespace")


#############################################################################
# Effacer
#############################################################################

def efface_tout() -> None:
    """
    Efface la fenêtre.
    """
    __img.clear()
    __canevas.canvas.delete("all")


def efface(objet) -> None:
    """
    Efface ``objet`` de la fenêtre.

    :param: objet ou étiquette d'objet à supprimer
    :type: ``int`` ou ``str``
    """
    if objet in __img:
        del __img[objet]
    __canevas.canvas.delete(objet)


#############################################################################
# Utilitaires
#############################################################################


def attente(temps) -> None:
    start = time()
    while time() - start < temps:
        mise_a_jour()


def capture_ecran(file) -> None:
    """
    Fait une capture d'écran sauvegardée dans ``file.png``.
    """
    __canevas.canvas.postscript(file=file + ".ps", height=__canevas.height,
                                width=__canevas.width, colormode="color")

    subprocess.call(
        "convert -density 150 -geometry 100% -background white -flatten"
        " " + file + ".ps " + file + ".png", shell=True)
    subprocess.call("rm " + file + ".ps", shell=True)


def touche_pressee(keysym) -> bool:
    """
    Renvoie `True` si ``keysym`` est actuellement pressée.
    :param keysym: symbole associé à la touche à tester.
    :return: `True` si ``keysym`` est actuellement pressée, `False` sinon.
    """
    return keysym in __canevas.pressed_keys


def entree_texte(x: float, y: float,
                 width: float, height: float,
                 police: str = "Courier",
                 justify: Literal['left', 'center', 'right'] = "center"
                 ) -> Entry:
    """
    Crée un champ de texte aux coordonnés x, y, ancrée en ``'nw'``.
    La taille du texte du champ peut être définie dans la chaîne,
    exemple: 'Courier 20'

    :param int x: Position sur l'axe x
    :param int y: Position sur l'axe y
    :param int width: Largeur du champ de texte
    :param int height: Hauteur du champ de texte
    :param str font: Police d'écriture
    :param str justify: Justification du texte.
    :return entry: Champ de texte
    """
    entry = Entry(__canevas.canvas, justify=justify, font=police)
    entry.place(x=x, y=y, width=width, height=height, anchor='nw')
    return entry


def detruit_entree_texte(boite: Entry) -> None:
    """
    Détruit le champ de textes "boite".
    """
    boite.destroy()
    __canevas.canvas.focus_set()


#############################################################################
# Gestions des évènements
#############################################################################


def donne_ev() -> Tuple[str, tkinter.Event]:
    """
    Renvoie immédiatement l'événement en attente le plus ancien,
    ou ``None`` si aucun événement n'est en attente.
    """
    if __canevas is None:
        raise FenetreNonCree(
            "La fenêtre n'a pas été créée avec la fonction \"cree_fenetre\".")
    if len(__canevas.ev_queue) == 0:
        return None
    else:
        return __canevas.ev_queue.popleft()


def attend_ev() -> Tuple[str, tkinter.Event]:
    """Attend qu'un événement ait lieu et renvoie le premier événement qui
    se produit."""
    while True:
        ev = donne_ev()
        if ev is not None:
            return ev
        mise_a_jour()


def attend_clic_gauche() -> Tuple[int, int]:
    """Attend qu'un clic gauche sur la fenêtre ait lieu et renvoie ses
    coordonnées. **Attention**, cette fonction empêche la détection d'autres
    événements ou la fermeture de la fenêtre."""
    while True:
        ev = donne_ev()
        if ev is not None and type_ev(ev) == 'ClicGauche':
            return abscisse(ev), ordonnee(ev)
        mise_a_jour()


def attend_fermeture() -> None:
    """Attend la fermeture de la fenêtre. Cette fonction renvoie None.
    **Attention**, cette fonction empêche la détection d'autres événements."""
    while True:
        ev = donne_ev()
        if ev is not None and type_ev(ev) == 'Quitte':
            ferme_fenetre()
            return
        mise_a_jour()


def type_ev(ev: Tuple[str, tkinter.Event]) -> str:
    """
    Renvoie une chaîne donnant le type de ``ev``. Les types
    possibles sont 'ClicDroit', 'ClicGauche', 'Touche' et 'Quitte'.
    Renvoie ``None`` si ``evenement`` vaut ``None``.
    """
    return ev if ev is None else ev[0]


def abscisse(ev: Tuple[str, tkinter.Event]) -> int:
    """
    Renvoie la coordonnée x associé à ``ev`` si elle existe, None sinon.
    """
    return attribut(ev, 'x')


def ordonnee(ev: Tuple[str, tkinter.Event]) -> int:
    """
    Renvoie la coordonnée y associé à ``ev`` si elle existe, None sinon.
    """
    return attribut(ev, 'y')


def touche(ev: Tuple[str, tkinter.Event]) -> str:
    """
    Renvoie une chaîne correspondant à la touche associé à ``ev``,
    si elle existe.
    """
    return attribut(ev, 'keysym')


def attribut(ev: Tuple[str, tkinter.Event], nom: str):
    if ev is None:
        raise TypeEvenementNonValide(
            "Accès à l'attribut", nom, 'impossible sur un événement vide')
    tev, ev = ev
    if hasattr(ev, nom):
        return getattr(ev, nom)
    else:
        raise TypeEvenementNonValide(
            "Accès à l'attribut", nom,
            'impossible sur un événement de type', tev)


def abscisse_souris() -> int:
    return __canevas.canvas.winfo_pointerx() - __canevas.canvas.winfo_rootx()


def ordonnee_souris() -> int:
    return __canevas.canvas.winfo_pointery() - __canevas.canvas.winfo_rooty()
