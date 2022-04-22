from bouton import Boutons

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
        'son', cfg,
        'Son!', 'Muet', unifier_texte=False
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
                print(click)
                print(cfg.son)
                if click not in {None, 'son'}:
                    return click

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()

if __name__ == '__main__':
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre, 'Here we go !')
    menu()