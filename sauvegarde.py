import json

from sqlalchemy import false
import selecteur
import cfg
import fltk
import graphiques
from bouton import Boutons
from plateau import Plateau


def check_in():
    global carte_save, historique_save, position_save
    file = json.load(open('savefile.json'))

    carte_save = file['carte']
    historique_save = file['historique']
    position_save = file['position']

def save_write(carte, historique, troupeau):
    with open("savefile.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data['carte'] = carte
    data['historique'] = historique_savewrite(historique)
    data['position'] = troupeau_savewrite(troupeau)

    with open("savefile.json", "w+") as jsonFile:
        jsonFile.write(json.dumps(data))

def troupeau_savewrite(troupeau):
    liste = []
    for mouton in troupeau:
        liste.append([mouton.y, mouton.x])
    return liste

def historique_savewrite(historique):
    liste = []
    for temps in historique:
        temp = []
        for mouton in temps:
            temp.append([mouton.y, mouton.x])
        liste.append(temp)

    return liste


def save_read():
    check_in()
    selecteur.modif_json(carte_save[0], carte_save[1])
    cfg.maj()
    plateau = Plateau(cfg.carte)
    plateau.historique_savewrite(historique_save)
    plateau.troupeau_savewrite(position_save)
     
    return plateau


def clear_save():
    save_write([], [], [])


def compare():
    print(carte_save, historique_save, position_save)
    print(carte_save != cfg.carte, historique_save!=[], position_save !=[])
    print(cfg.carte != carte_save and historique_save != [] and position_save != [])
    if carte_save != []:
        return cfg.carte != carte_save and historique_save != [] and position_save != []
    return False

def menu():
    boutons = Boutons((10,10))
    boutons.cree_bouton_texte(1, 1, 8, 1, "Attention")
    boutons.cree_bouton_texte(1, 2, 8, 2, "Une sauvegarde a été détectée.")
    boutons.cree_bouton_simple(1, 4, 8, 4, 'Continuer la partie', arrondi=0.75)
    boutons.cree_bouton_simple(1, 6, 8, 6, 'Ecraser la sauvegarde', arrondi=0.75)
    
    boutons.init()

    while True:
        try:
            fltk.efface_tout()
            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)
            graphiques.background("#3f3e47")
            boutons.grille.draw()
            click = boutons.dessiner_boutons(tev)

            if tev == 'Quitte':
                fltk.ferme_fenetre()
                exit()

            elif tev == "ClicGauche":
                if click not in {None}:
                    if click == "Continuer la partie":
                        return save_read()

                    elif click == "Ecraser la sauvegarde":
                        clear_save()
                        check_in()
                        return None



            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()



check_in()