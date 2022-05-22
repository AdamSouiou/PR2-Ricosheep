from plateau import Plateau
from bouton import Boutons
from typing import Callable, List, Tuple, Set
from random import randint
from solveur import iteratif
from math import ceil
import son
import graphiques
import fltk
import random
import editeur
import cfg


# Crash généré lors d'un random entre 5x5 et 8x8
def generation100() -> Plateau:
    """
    Créer un plateau dont les dimensions, le nombre de moutons et d'herbes
    est aléatoire et également resolubles

    :return Plateau: Plateau de jeu généré par la fonction.
    """
    global plateau
    test = False
    while not test:
        nb_colonnes = random.randint(4, 8)
        nb_lignes = random.randint(4, 8)

        plateau = []
        for _ in range(nb_lignes):
            ligne = []
            for _ in range(nb_colonnes):
                case = random.randint(1, 12)
                if case <= 5:
                    ligne.append(editeur.ETAT[0])
                elif case <= 10:
                    ligne.append(editeur.ETAT[1])
                elif case == 11:
                    ligne.append(editeur.ETAT[2])
                elif case == 12:
                    ligne.append(editeur.ETAT[3])
            plateau.append(ligne)
        test, chemin = editeur.test(plateau, False, False)
        if len(chemin) <= 3:
            test = False
    cfg.carte_lst = ['custom', 'Random.txt']
    return plateau


def map_dict(d: dict, func: Callable) -> None:
    """
    Applique une fonction à toutes les valeurs du dictionnaire.

    :param dict d: Dicionnaire à utiliser
    :param Callable func: Fonction à appliquer sur les valeurs du dictionnaire.
    """
    for cle, valeur in d.items():
        d[cle] = func(valeur)


def in_sets(elem: Tuple, sets: List[Set[Tuple]]) -> bool:
    """
    Renvoie vrai si ``elem`` est présent dans au
    moins un des itérables de la liste d'entrée.

    :param Tuple elem: Element a traiter
    :param List[Set[Tuple]] sets: Liste de sets à vérifier
    :return bool: Si l'élément est dans la liste.
    """
    for i_set in sets:
        if elem in i_set:
            return True
    return False


def set_aleatoire(nb_tuple: int,
                  max_y: int, max_x: int,
                  sets: List[Set[Tuple]]) -> set:
    """
    Renvoie un set aléatoire de tuple de positions, en s'assurant
    qu'aucune de ces nouvelles positions ne soient présente dans
    les itérables de la liste ``sets``.

    :param int nb_tuple: Nombre de tuples à générer
    :param int max_y: Position max sur la hauteur
    :param int max_x: Position max sur la longueur
    :param List[Set[Tuple]] sets: Liste de set à comparé
    :return set: Nouveau set généré par la fonction
    """
    new_set = set()
    while len(new_set) < nb_tuple:
        tup = (randint(0, max_y-1), randint(0, max_x-1))
        if (tup not in new_set
           and not in_sets(tup, sets)):
            new_set.add(tup)

    return new_set


def aleatoirecontrole(param: dict,
                      percent_buisson: Tuple[float, float]) -> Plateau:
    """
    Génère une map aléatoirement, respectent les conditions du dictionnaire
    params (nb_moutons, nb_herbes, nb_lignes, nb_colonnes, difficulte)

    :param dict param: Dictionnaire des paramètres pour réaliser la génération
    :param tuple percent_buisson: Tuple de nombre représentant
    le pourcentage min et max du nombre de buissons par rapport
    à l'espace vide restant après placement des herbes et moutons.
    :return Plateau: Plateau valide prêt à l'emploi
    """
    lignes, colonnes, nb_moutons, nb_herbes =\
        param['lignes'], param['colonnes'], param['moutons'], param['herbes']

    max_nb_buissons = lignes * colonnes - nb_herbes - nb_herbes
    buissons_min = int(max_nb_buissons * (percent_buisson[0] / 100))
    buissons_max = ceil(max_nb_buissons * (percent_buisson[1] / 100))

    while True:
        troupeau = set_aleatoire(nb_moutons, lignes, colonnes, [])
        herbes = set_aleatoire(nb_herbes, lignes, colonnes, [troupeau])
        buissons = set_aleatoire(
            randint(buissons_min, buissons_max),
            lignes, colonnes, [troupeau, herbes]
        )

        plateau = Plateau(
            '', test_mode=True,
            parsed_data=[troupeau, buissons, herbes, lignes, colonnes]
        )
        chemin, _ = iteratif(plateau, largeur=True)

        if chemin is not None and len(chemin) >= param['difficulte']:
            cfg.carte_lst = ['custom', 'Random.txt']
            return plateau


def menu_control():
    boutons = Boutons((10, 10))
    boutons.cree_bouton_texte(1, 2, 5, 2, "Nombre de lignes :", arrondi=0.75)
    boutons.entree_texte(7, 2, 8, 2, "lignes")

    boutons.cree_bouton_texte(1, 3, 5, 3, "Nombre de colonnes :", arrondi=0.75)
    boutons.entree_texte(7, 3, 8, 3, "colonnes")

    boutons.cree_bouton_texte(1, 4, 5, 4, "Nombre de moutons :", arrondi=0.75)
    boutons.entree_texte(7, 4, 8, 4, "moutons")

    boutons.cree_bouton_texte(1, 5, 5, 5, "Nombre de touffes :", arrondi=0.75)
    boutons.entree_texte(7, 5, 8, 5, "herbes")

    boutons.cree_bouton_texte(1, 6, 5, 6, "Nombre de coups :", arrondi=0.75)
    boutons.entree_texte(7, 6, 8, 6, "difficulte")

    boutons.cree_bouton_simple(2, 8, 7, 8, "Valider", arrondi=1)

    entiers_positifs = "Veuillez insérer que des entiers positifs !"
    boutons.cree_bouton_texte(1, 9, 8, 9, entiers_positifs,
                              invisible=True, couleur_texte='red')

    règle_de_jeuM = "Il vous faut au moins autant de moutons que d'herbes !"
    boutons.cree_bouton_texte(1, 9, 8, 9, règle_de_jeuM,
                              invisible=True, couleur_texte='red',
                              unifier_texte=False)

    règle_de_jeuT = "Le plateau doit pouvoir contenir tous les éléments!"
    boutons.cree_bouton_texte(1, 9, 8, 9, règle_de_jeuT,
                              invisible=True, couleur_texte='red',
                              unifier_texte=False)

    boutons.init()
    ev = None

    while True:
        fltk.efface_tout()
        graphiques.background("#3f3e47")
        boutons.dessiner_boutons(ev)

        ev = fltk.attend_ev()
        tev = fltk.type_ev(ev)
        click = boutons.nom_clic(ev)

        if tev == 'Quitte':
            boutons.destroy_entree_textes()
            graphiques.close()
        if tev == "Touche":
            if fltk.touche(ev) == "Escape":
                boutons.destroy_entree_textes()
                return

        if tev == "ClicGauche" and click is not None:
            son.sound('MenuAccept')

            params = {nom: entree.get()
                      for nom, entree in boutons.entrees_texte.items()}
            if all(n.isdecimal() for n in params.values()):
                map_dict(params, int)
                changement = True
            else:
                changement = False

            if changement:
                if all(n > 0 for n in params.values()):
                    boutons.boutons[entiers_positifs].invisible = True

                    if params['moutons'] < params['herbes']:
                        boutons.boutons[règle_de_jeuM].invisible = False
                        boutons.boutons[règle_de_jeuT].invisible = True

                    elif ((params['lignes'] * params['colonnes'])
                          <= (params['moutons'] + params['herbes'])):
                        boutons.boutons[règle_de_jeuT].invisible = False
                        boutons.boutons[règle_de_jeuM].invisible = True

                    else:
                        boutons.destroy_entree_textes()
                        return aleatoirecontrole(params, (20, 70))

                else:
                    boutons.boutons[entiers_positifs].invisible = False
                    boutons.boutons[règle_de_jeuT].invisible = True
                    boutons.boutons[règle_de_jeuM].invisible = True

        fltk.mise_a_jour()
