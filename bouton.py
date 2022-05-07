""" Forké de
PROJET 1, TP 11 GROUPE 4
Amal Abdallah, Nicolas Seban, Adam Souiou
"""
"""
PROJET 2
Amal Abdallah, Nicolas Seban, Adam Souiou
"""
# Sobre bibliothèque pour créer, gérer, et afficher des boutons,
# selon une grille
# Permet la création de boutons cliquables simples et de boutons
# booléens qui peuvent enregistrer leur état et l'afficher
# par leur couleur, et de boutons invisibles.

# A faire:
# - Mise en cache des boutons arrondis?
# - Bouton avec icône: Utiliser une police avec symboles?

from time import time
from pprint import pprint
from math import pi as PI, sin, cos
from numpy import linspace
from dataclasses import dataclass
from typing import Union, List, Dict
from grille import Grille
import cfg
import fltk


@dataclass
class Bouton:
    ax: float
    ay: float
    bx: float
    by: float
    format: tuple
    rayon = 0
    invisible = False
    factice = False


@dataclass
class BoutonTexte(Bouton):
    texte: str
    taille_texte = None
    unifier_texte = True
    marge_texte = 0.9
    police = 'Courier'
    couleur_texte = 'black'
    couleur_fond = 'white'
    centre_x = 0
    centre_y = 0


@dataclass
class BoutonSimple(BoutonTexte):
    enable_hovered = True
    couleur_hovered = '#848484'


@dataclass
class BoutonBooleen(BoutonTexte):
    object_ref: object
    attribute: str
    texte_actif: str
    texte_desactive: str
    couleur_actif = '#0a8029'
    couleur_hovered_actif = '#0b4f34'
    couleur_desactive = '#cf0e0e'
    couleur_hovered_desactive = '#941010'


class Boutons:
    boutons:       Dict[str, Bouton]
    grille:        Grille
    formats_texte: Dict
    time_start:    float

    __slots__ = tuple(__annotations__)
    
    def __init__(self, format_grille):
        """
        Initialise la grille selon laquelle seront positionnés les boutons.
        """
        self.time_start = time()
        self.boutons = {}
        self.grille = Grille(format_grille[0], format_grille[1],
                             marge_largeur=0.95, marge_hauteur=0.95,
                             grille_base=None,
                             grille_pos=(0, 0, cfg.largeur_fenetre, cfg.hauteur_fenetre),
                             carre=True)
        self.formats_texte = {}

    def init(self, unifier='format'):
        """
        Unifie la taille des textes des boutons, soit par rapport à leur
        format (ex: 2 boutons 4x1 auront la même taille de texte de 10,
        et 4 boutons de 8x2 auront la même taille de texte de 20),
        soit par rapport à l'instance (ex: Pour 2 boutons 4x1
        aura été calculé une taille de texte de 10, et pour 4 boutons de 8x2,
        une taille de texte de 20, mais après appel il seront unifiés à 10)

        Les boutons ayant la propriété ``unifier_texte`` désactivé sont
        ignorés.
        """
        for bouton in self.boutons.values():
            bouton.centre_x = (bouton.bx + bouton.ax) // 2
            bouton.centre_y = (bouton.by + bouton.ay) // 2
        
        self.unifier_taille_texte_format()
        if unifier == 'all':
            self.unifier_texte_texte_minimum()
        print(f'Boutons chargés en {time()-self.time_start:.3f}s')

    format_bouton = staticmethod(lambda ax, ay, bx, by: (bx - ax + 1, by - ay + 1))

    def cree_bouton_texte(self, ax: float, ay: float, bx: float, by: float,
                          texte: str, **kwargs) -> BoutonTexte:
        """
        Crée un bouton factice (ne change pas de couleur lors de son survol)
        à partir des positions des cases de la grille, avec comme
        texte : ``texte``.
    
        :param float ax: Abscisse de la case ``a`` de la grille, entre 0
        et la taille en largeur de la grille non-inclue
        :param float ay: Ordonnée de la case ``a`` de la grille entre 0
        et la taille en hauteur de la grille non-inclue
        :param float bx: Abscisse de la case ``b`` de la grille, entre 0
        et la taille en largeur de la grille
        :param float by: Ordonnée de la case ``b`` de la grille, entre 0
        et la taille en largeur de la grille
        :param str texte: Texte du bouton
    
        :param bool hovered: Optionnel, détermine si le bouton change de couleur
        lors  de son survol. Par défaut: ``True``
        :param str couleur_hovered: Optionnel, couleur du fond du bouton
        lors de son survol par la souris. Par défaut: ``'#848484'``
        :param str police: Optionnel, nom de la typographie à utiliser pour
        le texte du bouton. Par défaut, ``'Courier'``
        :param bool unifier_texte: Optionnel, spécifie si la taille de texte
        de ce bouton sera pris en compte lors de l'utilisation de
        la fonction unifier_taille_texte()
        :param bool invisible: Optionnel, rend le bouton invisible
        :param bool factice: Optionnel, si à ``True`` le bouton ne
        changera pas de couleur à son survol, et l'appel à dessiner_boutons()
        ne le mentionnera pas
    
        :return: Objet Bouton factice
        """
        bouton = BoutonTexte(
                    self.grille.cases[ay][ax].ax,
                    self.grille.cases[ay][ax].ay,
                    self.grille.cases[by][bx].bx,
                    self.grille.cases[by][bx].by,
                    self.format_bouton(ax, ay, bx, by),
                    texte
                 )
        self.parse_optionnal_args(kwargs, bouton)
        self.boutons[texte] = bouton
    
    
    def cree_bouton_invisible(self, ax: float, ay: float, bx: float, by: float,
                              identificateur: str) -> Bouton:
        """
        Crée un bouton invisible à partir des positions des cases de la grille,
        avec comme identificateur : ``identificateur``
    
        :param float ax: Abscisse de la case ``a`` de la grille, entre 0
        et la taille en largeur de la grille non-inclue
        :param float ay: Ordonnée de la case ``a`` de la grille entre 0
        et la taille en hauteur de la grille non-inclue
        :param float bx: Abscisse de la case ``b`` de la grille, entre 0
        et la taille en largeur de la grille
        :param float by: Ordonnée de la case ``b`` de la grille, entre 0
        et la taille en largeur de la grille
        :param str identificateur: Nom du bouton
        :return: Objet Bouton invisible
        """
        bouton = Bouton(
                    self.grille.cases[ay][ax].ax,
                    self.grille.cases[ay][ax].ay,
                    self.grille.cases[by][bx].bx,
                    self.grille.cases[by][bx].by,
                    self.format_bouton(ax, ay, bx, by),
                 )
        bouton.invisible = True
        self.boutons[identificateur] = bouton


    def cree_bouton_booleen(self,
            ax: float, ay: float, bx: float, by: float,
            attribut: str,
            object: object,
            texte_actif: str, texte_desactive: str,
            invert_color=False, **kwargs) -> BoutonBooleen:
        """
        Crée un bouton booléen à partir des positions des cases de la grille,
        et l'initialise à la valeur booléenne de l'attribut de l'objet.
        Le libellé du bouton sera ``texte_actif`` lorsque
        ce booléen vaut ``True``, sinon le libellé ``texte_desactive``.
    
        :param float ax: Abscisse de la case ``a`` de la grille, entre 0
        et la taille en largeur de la grille non-inclue
        :param float ay: Ordonnée de la case ``a`` de la grille entre 0
        et la taille en hauteur de la grille non-inclue
        :param float bx: Abscisse de la case ``b`` de la grille, entre 0
        et la taille en largeur de la grille
        :param float by: Ordonnée de la case ``b`` de la grille, entre 0
        et la taille en largeur de la grille
        :param str attribut: attribut de l'objet
        :param object: Objet contenant l'attribut booléen
        :param str texte_actif: Libellé du bouton à l'état actif
        :param str texte_desactive: Libellé du bouton à l'état désactivé
        :param bool invert_color: Inverse la couleur activé/désactivé
    
        :param str police: Optionnel, nom de la typographie à utiliser pour
        le texte du bouton. Par défaut, ``'Courier'``
        :param bool unifier_texte: Optionnel, spécifie si la
        taille de texte de ce bouton sera pris en compte lors de
        l'utilisation de la fonction unifier_taille_texte()
        :param bool invisible: Optionnel, rend le bouton invisible
        :param bool factice: Optionnel, si à ``True``,
        le bouton ne changera pas de couleur à son survol, et
        l'appel à dessiner_boutons() ne le mentionnera pas
    
        :return BoutonBooleen: Objet bouton booléen
        """
        bouton = BoutonBooleen(
                    self.grille.cases[ay][ax].ax,
                    self.grille.cases[ay][ax].ay,
                    self.grille.cases[by][bx].bx,
                    self.grille.cases[by][bx].by,
                    self.format_bouton(ax, ay, bx, by),
                    '',
                    object,
                    attribut,
                    texte_actif,
                    texte_desactive,
                 )
        self.parse_optionnal_args(kwargs, bouton)
        if invert_color:
            bouton.couleur_actif, bouton.couleur_desactive = \
                bouton.couleur_desactive, bouton.couleur_actif
    
            bouton.couleur_hovered_actif, bouton.couleur_hovered_desactive = \
                bouton.couleur_hovered_desactive, bouton.couleur_hovered_actif
        self.boutons[attribut] = bouton
    
    
    def cree_bouton_simple(self, ax: float, ay: float, bx: float, by: float,
                           texte: str, **kwargs) -> BoutonSimple:
        """
        Crée un bouton simple, c'est à dire survolable, à partir des
        positions des cases de la grille.
    
        :param float ax: Abscisse de la case ``a`` de la grille, entre 0
        et la taille en largeur de la grille non-inclue
        :param float ay: Ordonnée de la case ``a`` de la grille entre 0
        et la taille en hauteur de la grille non-inclue
        :param float bx: Abscisse de la case ``b`` de la grille, entre 0
        et la taille en largeur de la grille
        :param float by: Ordonnée de la case ``b`` de la grille, entre 0
        et la taille en largeur de la grille
        :param str texte: Nom du bouton
    
        :param bool hovered: Optionnel, détermine si le bouton change
        de couleur lors de son survol. Par défaut: ``True``
        :param str couleur_hovered: Optionnel, couleur du fond du bouton
        lors de son survol par la souris. Par défaut: ``'#848484'``
        :param str police: Optionnel, nom de la typographie à utiliser
        pour le texte du bouton. Par défaut, ``'Courier'``
        :param bool unifier_texte: Optionnel, spécifie si la
        taille de texte de ce bouton sera pris en compte lors de l'utilisation
        de la fonction unifier_taille_texte()
        :param bool invisible: Optionnel, rend le bouton invisible
        :param bool factice: Optionnel, si à ``True``, le bouton ne
        changera pas de couleur à son survol, et l'appel à dessiner_boutons()
        ne le mentionnera pas
    
        :return Bouton: Objet Bouton
        """
        bouton = BoutonSimple(
                    self.grille.cases[ay][ax].ax,
                    self.grille.cases[ay][ax].ay,
                    self.grille.cases[by][bx].bx,
                    self.grille.cases[by][bx].by,
                    self.format_bouton(ax, ay, bx, by),
                    texte
                 )
        self.parse_optionnal_args(kwargs, bouton)
        self.boutons[texte] = bouton

    @staticmethod
    def rectangle_arrondi(bouton, precision):
        bouton.polygone = []
        largeur_bouton = (bouton.bx - bouton.ax)
    
        for i in linspace(PI, PI/2, precision+1): # Top Left
            bouton.polygone.append((
                    (bouton.ax + bouton.rayon)                  + cos(i) * bouton.rayon,
                    (bouton.ay + bouton.rayon)                  - sin(i) * bouton.rayon
                ))
    
        for i in linspace(PI/2, PI, precision+1): # Top Right
            bouton.polygone.append((
                    (bouton.ax - bouton.rayon + largeur_bouton) - cos(i) * bouton.rayon,
                    (bouton.ay + bouton.rayon)                  - sin(i) * bouton.rayon
                ))
    
        for i in linspace(0, PI/2, precision+1): # Bottom Right
            bouton.polygone.append((
                    (bouton.bx - bouton.rayon)                  + cos(i) * bouton.rayon,
                    (bouton.by - bouton.rayon)                  + sin(i) * bouton.rayon
                ))
    
        for i in linspace(PI/2, 0, precision+1): # Bottom Left
            bouton.polygone.append((
                    (bouton.bx + bouton.rayon - largeur_bouton) - cos(i) * bouton.rayon,
                    (bouton.by - bouton.rayon)                  + sin(i) * bouton.rayon
                ))
        # print(f'Nombre de points générés: {len(bouton.polygone)}')

    
    def parse_optionnal_args(self, args: dict, bouton):
        """
        Parsing des arguments optionnels, et valeurs par défaut.
        """
        if 'arrondi' not in args:
            args['arrondi'] = 0
    
        for arg, value in args.items():
            if type(bouton) == BoutonSimple:
                if arg == 'hovered':
                    bouton.enable_hovered = value
                elif arg == 'couleur_hovered':
                    bouton.couleur_hovered = value
            if arg == 'marge_texte':
                bouton.marge_texte = value
            elif arg == 'unifier_texte':
                bouton.unifier_texte = value
            elif arg == 'police':
                bouton.police = value
            elif arg == 'invisible':
                bouton.invisible = value
            elif arg == 'factice':
                bouton.factice = value
            elif arg == 'arrondi':
                bouton.rayon = (bouton.by - bouton.ay)/2 * value
                precision = int(bouton.rayon / 2)
                self.rectangle_arrondi(bouton, precision)
    
            else:
                raise KeyError(f"L'argument {arg} n'existe pas, ou le bouton de \
                            type {type(bouton)} ne possède pas la propriété {arg}")

    @staticmethod
    def get_len_texte(bouton):
        return (max(len(bouton.texte_actif), len(bouton.texte_desactive)) if
                type(bouton) is BoutonBooleen else len(bouton.texte))

    def unifier_taille_texte_format(self) -> None:
        """
        Calcule la taille des textes des boutons, de manière à limiter le nombre d'appels
        à la fonction ``taille_texte_bouton`` qui fait appel à ``fltk.taille_texte``.
        En effet, cette fonction est très coûteuse, car adapter le texte d'un
        bouton nécessite d'incrémenter progressivement la taille du texte
        jusqu'à son dépassement, et de plus, la taille de l'écran pouvant
        augmenter, les boutons suivent également.
        Ainsi on calcule pour chaque format de bouton, la taille
        du texte maximal qu'il peut recevoir, en se réfèrant au
        texte le plus long que ce format recevra.
        """

        for nom, bouton in self.boutons.items():
            if type(bouton) is Bouton: continue
            len_texte = self.get_len_texte(bouton)

            if bouton.format in self.formats_texte:
                if len_texte > self.formats_texte[bouton.format]['len_texte']:
                    self.formats_texte[bouton.format] = {'nom': nom, 'len_texte': len_texte}
            else:
                self.formats_texte[bouton.format] = {'nom': nom, 'len_texte': len_texte}

        for max_text in self.formats_texte.values():
            bouton = self.boutons[max_text['nom']]
            taille = self.taille_texte_bouton(bouton)
            bouton.taille_texte = taille
            self.formats_texte[bouton.format]['taille_texte'] = taille

        for name, bouton in self.boutons.items():
            if type(bouton) is Bouton: continue
            bouton.taille_texte = (
                self.formats_texte[bouton.format]['taille_texte'] if bouton.unifier_texte
                else self.taille_texte_bouton(bouton))

    def unifier_texte_texte_minimum(self):
        """
        Minimise la taille du texte de tous les
        boutons de formats différents à une taille minimale.
        Si la propriété ``unifier_texte`` d'un bouton est désactivée,
        il sera ignoré.
        """
        taille_min = min(
            [format_bouton['taille_texte']\
             for format_bouton in self.formats_texte.values()]
        )
        for bouton in self.boutons.values():
            if bouton.unifier_texte:
                bouton.taille_texte = taille_min
    
    @staticmethod
    def taille_texte_bouton(bouton: Union[BoutonSimple, BoutonBooleen]) -> int:
        """
        Détermine une taille de texte optimisé pour le bouton d'entrée
    
        :param Bouton bouton: Objet Bouton
        :return int: Taille du texte à utiliser
        """
    
        hauteur_bouton = (bouton.by - bouton.ay) * bouton.marge_texte
        largeur_bouton = (bouton.bx - bouton.ax) * bouton.marge_texte
        taille_texte = 5

        while True:
            if type(bouton) == BoutonBooleen:
                largeur_hauteur = max(
                    fltk.taille_texte(
                        bouton.texte_actif, bouton.police, taille_texte
                    ),
                    fltk.taille_texte(
                        bouton.texte_desactive, bouton.police, taille_texte
                    )
                )
            else:
                largeur_hauteur = fltk.taille_texte(
                    bouton.texte, bouton.police, taille_texte
                )
    
            if (largeur_hauteur[0] > largeur_bouton
               or largeur_hauteur[1] > hauteur_bouton):
                break
            taille_texte += 2

        # print(f'Appel de taille_texte_bouton pour : {type(bouton)} et de format {bouton.format}')
        
        return taille_texte-1

    @staticmethod
    def dessiner_bouton(bouton: Bouton, survole: bool) -> bool:
        """
        Dessine un bouton et change sa couleur lors de son survol
        par la souris, si il n'est pas invisible. Et dans le cas d'un
        bouton booléen, change sa couleur en fonction de son attribut ``etat``,
        et s'il a été cliqué, permute sa valeur.
        Renvoie ``True`` si le bouton à été survolé.
    
        :param Bouton bouton: Objet Bouton
        :param str tev: Type de l'évènement fltk
        :return bool: Bouton survolé
        """
        if bouton.invisible:
            return
        if type(bouton) is BoutonBooleen:
            etat = getattr(bouton.object_ref, bouton.attribute)
            remplissage_actif = (bouton.couleur_hovered_actif if etat
                                 else bouton.couleur_hovered_desactive)
            remplissage = (bouton.couleur_actif if etat
                           else bouton.couleur_desactive)
        elif type(bouton) is BoutonSimple and bouton.enable_hovered:
            remplissage = bouton.couleur_fond
            remplissage_actif = (bouton.couleur_hovered if not bouton.factice
                                 else remplissage)
        else:
            remplissage = bouton.couleur_fond
            remplissage_actif = remplissage

        fltk.polygone(
            bouton.polygone,
            'black',
            remplissage=remplissage,
            remplissage_actif=remplissage_actif
        )
        if not isinstance(bouton, BoutonTexte): return
        fltk.texte(
            bouton.centre_x, bouton.centre_y,
            (bouton.texte_actif if etat else bouton.texte_desactive)
            if type(bouton) == BoutonBooleen else bouton.texte,
            bouton.couleur_texte, 'center',
            bouton.police, bouton.taille_texte
        )
    
    def dessiner_boutons(self, ev=None) -> str:
        """
        Dessine tous les boutons de l'instance, et renvoie également l'identificateur
        d'un bouton si celui-ci est survolé, et ``None`` si aucun ne l'a été.

        :return str: Texte du bouton qui a été survolé
        """
    
        nom_bouton_survole = None
        deja_survole = False
        for identificateur, bouton in self.boutons.items():
            survole = False
            # Evite de tester si un bouton est survolé, si
            # un bouton à déjà été survolé.
            if not deja_survole:
                survole = self.curseur_sur_bouton(bouton, ev)
                if survole and type(bouton) is not BoutonTexte:
                    deja_survole = True
                    if not bouton.factice:
                        nom_bouton_survole = identificateur
            self.dessiner_bouton(bouton, survole)
    
        return nom_bouton_survole

    def nom_clic(self, ev):
        for identificateur, bouton in self.boutons.items():
            if self.curseur_sur_bouton(bouton, ev):
                if isinstance(bouton, BoutonBooleen):
                    etat = getattr(bouton.object_ref, bouton.attribute)
                    if fltk.type_ev(ev) == 'ClicGauche':
                        setattr(bouton.object_ref, bouton.attribute, not etat)
                return identificateur
        return None

    @staticmethod
    def curseur_sur_bouton(bouton: Bouton, ev: tuple) -> bool:
        """
        Détecte si le curseur est situé sur le rectangle formé par
        ses composantes ax, ay, bx et by, définies dans l'objet Bouton
        et renvoie ``True`` si tel est le cas.
    
        :param Bouton: Objet ``Bouton``
        :return bool:
        """
        if ev is None: return False
        return ((bouton.ax <= fltk.abscisse(ev) <= bouton.bx)
                and (bouton.ay <= fltk.ordonnee(ev) <= bouton.by))
    
    def intervertir_pos_boutons(self, bouton1_id: str, bouton2_id: str):
        """
        Intervertit la position de deux boutons
        """
        bouton1, bouton2 = self.boutons[bouton1_id], self.boutons[bouton2_id]
        bouton1.ay, bouton1.by, bouton2.ay, bouton2.by\
            = bouton2.ay, bouton2.by, bouton1.ay, bouton1.by
    
        bouton1.ax, bouton1.bx, bouton2.ax, bouton2.bx\
            = bouton2.ax, bouton2.bx, bouton1.ax, bouton1.bx
    
        return None
