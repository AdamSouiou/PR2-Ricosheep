from bouton import Boutons
from plateau import Plateau
import graphiques
import cfg
import fltk
import selecteur
import sauvegarde
import editeur
import son


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
            #boutons.grille.draw()
            click = boutons.dessiner_boutons(tev)

            if tev == 'Quitte':
                fltk.ferme_fenetre()
                exit()

            elif tev == "Touche":
                print(fltk.touche(ev))

            elif tev == "ClicGauche":
                if click in {'Jouer', 'Niveaux', 'Editeur de Niveaux'}:
                    plateau = None
                    if sauvegarde.est_valide():
                        plateau = sauvegarde.menu()
                    
                    if click == "Jouer":
                        son.sound('MenuOk')
                        return plateau or Plateau(cfg.carte)
                    elif click == "Niveaux":
                        son.sound('Menubeep')
                        selecteur.menu()    
                        cfg.maj()
                    elif click == "Editeur de Niveaux":
                        son.sound('Menubeep')
                        print("bonjour")
                        editeur.debut()
                        print(plateau)
                elif click != {None}:
                    son.toggle_sound()

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()

if __name__ == "__main__":
    fltk.cree_fenetre(500, 500)
    menu()