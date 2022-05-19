import json
from os import path
from json.decoder import JSONDecodeError
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


def check_in():
    global save
    try:
        with open('savefile.json') as file:
            try:
                save = json.load(file)
            except JSONDecodeError:
                print("La sauvegarde lue est incorrecte, réinitialisation du fichier")
                clear_save()
    except FileNotFoundError:
        print("La sauvegarde n'existe plus !, réinitialisation du fichier")
        clear_save()

def clear_save():
    save_write([], [], [])


def save_write(carte, historique, troupeau):
    global save
    with open("savefile.json", "w+") as jsonFile:
        save['carte'] = carte
        save['historique'] = historique
        save['position'] = troupeau
        jsonFile.write(json.dumps(save, indent=2, cls=SaveEncoder))


def save_read():
    check_in()
    selecteur.modif_json(save['carte'][0], save['carte'][1])
    cfg.maj()
    plateau = Plateau(cfg.carte)
    plateau.historique_savewrite(save['historique'])
    plateau.troupeau_savewrite(save['position'])
    plateau.reposition_moutons()
     
    return plateau


def est_valide():
    check_in()
            
    if save['carte'] and not path.exists(path.join('maps', *save['carte'])):
        clear_save()
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
                        clear_save()
                        check_in()
                        return None

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()
