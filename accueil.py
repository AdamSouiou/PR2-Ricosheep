from bouton import Boutons
import graphiques
import cfg
import fltk
import selecteur


def menu():

    boutons = Boutons((10,10))
    boutons.cree_bouton_simple(1, 4, 8, 4, 'Jouer', arrondi=0.5)
    boutons.cree_bouton_simple(1, 6, 8, 6, 'Niveaux')
    boutons.cree_bouton_simple(1, 8, 8, 8, 'Options')
    boutons.cree_bouton_booleen(
        9, 9, 9, 9,
        'son', cfg,
        'Son!', 'Muet', unifier_texte=False, arrondi=1
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
                if click not in {None, 'son'}:
                    if click == "Jouer":
                        return click
                    elif click == "Niveaux":
                        selecteur.menu()
                        cfg.maj()


            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()

if __name__ == '__main__':
    fltk.cree_fenetre(cfg.largeur_fenetre, cfg.hauteur_fenetre, 'Here we go !')
    menu()