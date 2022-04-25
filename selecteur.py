import os
import json
from sympy import false
from bouton import Boutons
import graphiques
import cfg
import fltk



def menu():
    split = 0
    directory = ""
    racine = os.listdir("maps")
    choix = None
    boutons = init_boutons(split, directory)

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
                if click not in {None, "Valider", choix}:
                    if click == "=>":
                        split += 1

                    elif click == "<=":
                        split -= 1


                    elif click == "\...":
                        directory = ""

                    elif click in racine:
                        directory = click


                    else:
                        choix = modif_json(directory, click)


                    boutons = init_boutons(split, directory, choix)

                if click == "Valider" and choix != None:
                    return choix

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()



def init_boutons( split = 0, directory = "", choix = None):
    dossiers = os.listdir(os.path.join("maps", directory))
    
    boutons = Boutons((10,10))

    if directory != "":
        boutons.cree_bouton_simple(5, 1, 8, 1, "\...")

    if choix:
        boutons.cree_bouton_texte(1, 9, 8, 9, choix, unifier_texte=False)

    if len(dossiers) <= 6:
        for i in range(len(dossiers)):
            boutons.cree_bouton_simple(1, 1+i, 4, 1+i, dossiers[i])    

    else:
        if split > 0:
            dos = dossiers[5*split:5*(split+1)]
            boutons.cree_bouton_simple(1, 6, 2, 6, "<=")

            if len(dossiers) > 5*(split+1):
                boutons.cree_bouton_simple(3, 6, 4, 6, "=>")

        else:
            dos = dossiers[:5]
            boutons.cree_bouton_simple(3, 6, 4, 6, "=>")
        for i in range(len(dos)):
            boutons.cree_bouton_simple(1, 1+i, 4, 1+i, dos[i])


    boutons.cree_bouton_simple(1, 8, 4, 8, "Valider")

    boutons.init()
    return boutons

def modif_json(directory, file):
    
    jsonFile = open("config.json", "r")
    data = json.load(jsonFile)
    jsonFile.close()

    data['carte'][0] = directory
    data['carte'][1] = file

    jsonFile = open("config.json", "w+")
    jsonFile.write(json.dumps(data, indent=4))
    jsonFile.close()


    return str(directory + "\\" + file)






if __name__ == '__main__':
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre, 'Here we go !')
    menu()