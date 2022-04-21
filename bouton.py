"""
PROJET 1, TP 11 GROUPE 4
Amal Abdallah, Nicolas Seban, Adam Souiou
"""
"""
PROJET 2
Amal Abdallah, Nicolas Seban, Adam Souiou
"""
# Sobre bibliothèque pour créer, gérer, et afficher des boutons,
# selon une grille
# Permet la création de boutons cliquables simples, de boutons
# booléens qui peuvent enregistrer leur état et l'afficher
# par leur couleur, et de boutons invisibles.

# A faire:
# - Boutons arrondis (peu performant car nécessite 4 appels à circle + 1 rectangle)
# - Bouton ronds
# - Bouton avec icône

from dataclasses import dataclass
from typing import Union
from grille import Grille
import cfg
import fltk


@dataclass
class Bouton:
    ax: float
    ay: float
    bx: float
    by: float
    invisible = False
    factice = False


@dataclass
class BoutonTexte(Bouton):
    texte: str
    taille_texte = None
    unifier_texte = True
    marge_texte = 0.9
    police = 'Biometric Joe'
    couleur_texte = 'black'
    couleur_fond = 'white'


@dataclass
class BoutonSimple(BoutonTexte):
    enable_hovered = True
    couleur_hovered = '#848484'


@dataclass
class BoutonBooleen(BoutonTexte):
    identificateur: str
    etat: bool
    texte_actif: str
    texte_desactive: str
    couleur_actif = '#0a8029'
    couleur_hovered_actif = '#0b4f34'
    couleur_desactive = '#cf0e0e'
    couleur_hovered_desactive = '#941010'


class Boutons:
    def __init__(self, format_grille):
        """
        Initialise la grille selon laquelle seront positionnés les boutons.
        """
        self.boutons = {}
        self.grille = Grille(format_grille[0], format_grille[1],
                             marge_largeur=0.95, marge_hauteur=0.95,
                             grille_base=None,
                             grille_pos=(0, 0, cfg.largeur_fenetre, cfg.hauteur_fenetre),
                             carre=True)

    def init(self):
        """
        Unifie la taille des textes de tous les boutons de l'instance, à la
        plus petite rencontrée.
        """
        self.unifier_taille_texte()

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
        le texte du bouton. Par défaut, ``'Biometric Joe'``
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
                    texte,
                 )
        self.parse_optionnal_args(kwargs, bouton)
    
        bouton.taille_texte = self.taille_texte_bouton(bouton)
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
                 )
        bouton.invisible = True
        self.boutons[identificateur] = bouton


    def cree_bouton_booleen(self,
            ax: float, ay: float, bx: float, by: float,
            identificateur: str,
            etat: bool,
            texte_actif: str, texte_desactive: str,
            invert_color=False, **kwargs) -> BoutonBooleen:
        """
        Crée un bouton booléen à partir des positions des cases de la grille,
        et l'initialise à la valeur du booléen ``etat``.
        Le libellé du bouton sera ``texte_actif`` lorsque
        l'attribut ``etat`` du bouton vaut ``True``, sinon
        le libellé ``texte_desactive``.
    
        :param float ax: Abscisse de la case ``a`` de la grille, entre 0
        et la taille en largeur de la grille non-inclue
        :param float ay: Ordonnée de la case ``a`` de la grille entre 0
        et la taille en hauteur de la grille non-inclue
        :param float bx: Abscisse de la case ``b`` de la grille, entre 0
        et la taille en largeur de la grille
        :param float by: Ordonnée de la case ``b`` de la grille, entre 0
        et la taille en largeur de la grille
        :param str identificateur: Nom du bouton
        :param str texte_actif: Libellé du bouton à l'état actif
        :param str texte_desactive: Libellé du bouton à l'état désactivé
        :param bool invert_color: Inverse la couleur activé/désactivé
    
        :param str police: Optionnel, nom de la typographie à utiliser pour
        le texte du bouton. Par défaut, ``'Biometric Joe'``
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
                    '',
                    identificateur,
                    etat,
                    texte_actif,
                    texte_desactive,
                 )
        self.parse_optionnal_args(kwargs, bouton)
        if invert_color:
            bouton.couleur_actif, bouton.couleur_desactive = \
                bouton.couleur_desactive, bouton.couleur_actif
    
            bouton.couleur_hovered_actif, bouton.couleur_hovered_desactive = \
                bouton.couleur_hovered_desactive, bouton.couleur_hovered_actif
    
        bouton.taille_texte = self.taille_texte_bouton(bouton)
    
        self.boutons[identificateur] = bouton
    
    
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
        pour le texte du bouton. Par défaut, ``'Biometric Joe'``
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
                    texte,
                 )
        self.parse_optionnal_args(kwargs, bouton)
    
        bouton.taille_texte = self.taille_texte_bouton(bouton)
    
        self.boutons[texte] = bouton

    
    def parse_optionnal_args(self, args: dict, bouton):
        """
        Parsing des arguments optionnels pour les fonctions
        cree_bouton_simple() et cree_bouton_factice()
        """
    
        for arg, value in args.items():
            if type(bouton) == BoutonSimple:
                if arg == 'hovered':
                    bouton.enable_hovered = value
                    break
                elif arg == 'couleur_hovered':
                    bouton.couleur_hovered = value
                    break
            if arg == 'unifier_texte':
                bouton.unifier_texte = value
                break
            elif arg == 'police':
                bouton.police = value
            elif arg == 'invisible':
                bouton.invisible = value
            elif arg == 'factice':
                bouton.factice = value
    
            else:
                raise KeyError(f"L'argument {arg} n'existe pas, ou le bouton de \
                            type {type(bouton)} ne possède pas la propriété {arg}")
    
    
    def unifier_taille_texte(self) -> None:
        """
        Unifie la taille des textes de chaque bouton de l'instance Bouton
        à la plus petite taille de texte rencontrée
        """
        
        taille_min = float('inf')
        for bouton in self.boutons.values():
    
            if (bouton.unifier_texte and (not bouton.invisible)
               and (bouton.taille_texte < taille_min)):
    
                taille_min = bouton.taille_texte
    
        for bouton in self.boutons.values():
    
            if (not bouton.invisible) and bouton.unifier_texte:
                bouton.taille_texte = taille_min
    
        return None
    
    
    def dessiner_bouton(self, bouton: Bouton, survole: bool, tev: str) -> bool:
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

        if bouton.factice:
            survole = False
    
        if not bouton.invisible:
            if type(bouton) == BoutonBooleen:
                if survole:
                    if bouton.etat:
                        remplissage = bouton.couleur_hovered_actif
                    else:
                        remplissage = bouton.couleur_hovered_desactive
                    if tev == 'ClicGauche':
                        bouton.etat ^= 1
                else:
                    if bouton.etat:
                        remplissage = bouton.couleur_actif
                    else:
                        remplissage = bouton.couleur_desactive
            else:
                if (survole
                   and (type(bouton) != BoutonTexte and bouton.enable_hovered)):
    
                    remplissage = bouton.couleur_hovered
                else:
                    remplissage = bouton.couleur_fond
    
            fltk.rectangle(
                bouton.ax, bouton.ay,
                bouton.bx, bouton.by,
                'black',
                remplissage
            )
            fltk.texte(
                (bouton.ax + bouton.bx)/2, (bouton.ay + bouton.by)/2,
                (bouton.texte_actif if bouton.etat else bouton.texte_desactive)
                if type(bouton) == BoutonBooleen else bouton.texte,
                bouton.couleur_texte, 'center',
                bouton.police, bouton.taille_texte
            )
    
        return survole
    
    
    def dessiner_boutons(self, tev, design_mode=False) -> str:
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
                survole = self.curseur_sur_bouton(bouton)
                if survole:
                    deja_survole = True
                    nom_bouton_survole = identificateur
            self.dessiner_bouton(bouton, survole, tev)
    
        return nom_bouton_survole

    
    def curseur_sur_bouton(self, bouton: Bouton) -> bool:
        """
        Détecte si le curseur est situé sur le rectangle formé par
        ses composantes ax, ay, bx et by, définies dans l'objet Bouton
        et renvoie ``True`` si tel est le cas.
    
        :param Bouton: Objet ``Bouton``
        :return bool:
        """
        return ((bouton.ax <= fltk.abscisse_souris() <= bouton.bx)
                and (bouton.ay <= fltk.ordonnee_souris() <= bouton.by))
    
    
    def taille_texte_bouton(self, bouton: Union[BoutonSimple, BoutonBooleen]) -> int:
        """
        Détermine une taille de texte optimisé pour le bouton
    
        :param Bouton bouton: Objet Bouton
        :return int: Taille du texte à utiliser
        """
    
        hauteur_bouton = (bouton.by - bouton.ay)*bouton.marge_texte
        largeur_bouton = (bouton.bx - bouton.ax)*bouton.marge_texte
        taille_texte = 1
    
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
            taille_texte += 1
    
        return taille_texte
    
    
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
