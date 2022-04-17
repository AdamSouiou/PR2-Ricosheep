from bouton import Boutons

import graphiques
import cfg
import fltk

def menu():

    boutons = Boutons((10,10))
    boutons.cree_bouton_simple(1, 5, 8, 5, 'Jouer')
    boutons.cree_bouton_simple(1, 7, 8, 7, 'Options')
    boutons.cree_bouton_booleen(
        9, 9, 9, 9,
        'Son', True, 'Son!', 'Muet', unifier_texte=False
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
                print(f"Etat du son : {boutons.boutons['Son'].etat}")
                if click not in {'Son'}:
                    return click

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()

if __name__ == '__main__':
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre, 'Here we go !')
    menu()