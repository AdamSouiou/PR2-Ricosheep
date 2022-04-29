from bouton import Boutons
import graphiques
import cfg
import fltk
import selecteur
import sauvegarde
import editeur


def menu():
    boutons = Boutons((10,10))
    boutons.cree_bouton_simple(1, 2, 8, 2, "Editeur de Niveaux", arrondi = 0.75)
    boutons.cree_bouton_simple(1, 4, 8, 4, 'Jouer', arrondi=0.75)
    boutons.cree_bouton_simple(1, 6, 8, 6, 'Niveaux', arrondi=0.75)
    boutons.cree_bouton_simple(1, 8, 8, 8, 'Options', arrondi=0.75)
    
    boutons.cree_bouton_booleen(
        9, 9, 9, 9,
        'son', cfg,
        'Son!', 'Muet', arrondi=1, marge_texte=0.8
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
                        return click, None
                    elif click == "Niveaux":
                        if sauvegarde.compare():
                            choix = sauvegarde.menu()
                            if choix is not None:
                                return "Jouer", choix
                        selecteur.menu()    
                        cfg.maj()
                    elif click == "Editeur de Niveaux":
                        plateau = editeur.debut()
                        print(plateau)


            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()