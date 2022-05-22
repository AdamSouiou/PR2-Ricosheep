import json
from os import path
from json.decoder import JSONDecodeError
from typing import List, Tuple
from ricosheep import boutons_jeu_init
import selecteur
import cfg
import fltk
import graphiques
from bouton import Boutons
from plateau import Plateau
from mouton import Mouton


save = {}


class SaveEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Mouton):
            return [obj.y, obj.x]
        return json.JSONEncoder.default(self, obj)


def check_in() -> None:
    """
    Essaye de lire le fichier savefile.json et l'enregistre
    dans la variable global "save" pour pouvoir encoder la sauvegarde.
    En cas d'echec, réinitialise le fichier de sauvegarde.
    """
    global save
    try:
        with open('savefile.json') as file:
            try:
                save = json.load(file)
            except JSONDecodeError:
                print("La sauvegarde lue est incorrecte,\
                      réinitialisation du fichier")
                save_write([], [], [])
    except FileNotFoundError:
        print("La sauvegarde n'existe plus !, réinitialisation du fichier")
        save_write([], [], [])


def save_write(carte: List[str],
               historique: List[Tuple[Mouton]],
               troupeau: List[Mouton]) -> None:
    """
    Écris savefile.json avec les paramètres donné.

    :param List[str] carte: Liste du sous-dossier
    et niveau pour la carte
    :param List[Tuple[Mouton]] historique: Liste de
    l'historique des moutons pendant toute la partie.
    :param List[Mouton] troupeau: Liste des objets moutons du jeu.
    """
    global save
    with open("savefile.json", "w+") as jsonFile:
        save['carte'] = carte
        save['historique'] = historique
        save['position'] = troupeau
        jsonFile.write(json.dumps(save, cls=SaveEncoder))


def save_read() -> Tuple[Plateau, Boutons]: 
    """
    Lit le fichier savefile.json pour récupérer les
    informations de la sauvegarde effectué précédemment.

    :return Plateau: Plateau de jeu
    :return Boutons: Boutons de jeu
    """
    check_in()
    selecteur.modif_json(save['carte'][0], save['carte'][1])
    cfg.maj()
    boutons_jeu = boutons_jeu_init()
    plateau = Plateau(
        cfg.carte,
        grille_base=boutons_jeu.grille,
        grille_pos=(0,0,15,22)
    )
    plateau.historique_savewrite(save['historique'])
    plateau.troupeau_savewrite(save['position'])
    plateau.reposition_moutons()
     
    return plateau, boutons_jeu


def est_valide() -> bool:
    """
    Vérifie si la sauvegarde est valide, puis si chaque élément
    présent dans la sauvegarde est égal à la liste vide.
    """
    check_in()
            
    if save['carte'] and not path.exists(path.join('maps', *save['carte'])):
        save_write([],[],[])
        raise FileNotFoundError

    return bool(save['carte'] and save['historique'] and save['position'])


def menu():
    boutons = Boutons((10,10))
    boutons.cree_bouton_texte(1, 1, 8, 1, "Attention !")
    boutons.cree_bouton_texte(1, 2, 8, 2, "Une sauvegarde a été détectée.")
    boutons.cree_bouton_simple(1, 4, 8, 4, 'Continuer la partie', arrondi=0.75)
    boutons.cree_bouton_simple(1, 6, 8, 6, 'Ecraser la sauvegarde', arrondi=0.75)
    
    boutons.init()
    ev = None

    while True:
        try:        
            fltk.efface_tout()
            graphiques.background("#3f3e47")
            boutons.dessiner_boutons(ev)
            
            ev = fltk.attend_ev()
            tev = fltk.type_ev(ev)
            click = boutons.nom_clic(ev)

            if tev == 'Quitte':
                fltk.ferme_fenetre()
                exit()

            elif tev == "ClicGauche":
                if click is not None:
                    if click == "Continuer la partie":
                        return save_read()

                    elif click == "Ecraser la sauvegarde":
                        save_write([],[],[])
                        check_in()
                        return None, None

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()
