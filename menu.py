from bouton import Boutons
from grille import Grille

import graphiques
import cfg
import fltk

def menu():

    boutons = Boutons((10,10))
    boutons.cree_bouton_simple(1, 4, 8, 4, 'Jouer')
    boutons.cree_bouton_simple(1, 6, 8, 6, 'Editeur')
    boutons.cree_bouton_simple(1, 8, 8, 8, 'Options')
    boutons.cree_bouton_booleen(
        9, 9, 9, 9,
        'Son', True, 'Son!', 'Muet', unifier_texte=False
    )
    boutons.cree_bouton_booleen(
        0, 9, 0, 9,
        'Precalcul', cfg.precalcul_perdant, 'Precalcul', 'Normal', unifier_texte=False
    )
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
                cfg.precalcul_perdant = boutons.boutons['Precalcul'].etat
                print(click)
                if click not in {None, 'Son', 'Precalcul'}:
                    return click

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()

if __name__ == '__main__':
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre, 'Here we go !')
    menu()
