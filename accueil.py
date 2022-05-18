from bouton import Boutons
from plateau import Plateau, FichierInvalide
from ricosheep import jeu
import graphiques
import cfg
import fltk
import selecteur
import sauvegarde
import editeur
import son


def menu():
    son.song("Wait")
    boutons = Boutons((10,10))
    boutons.cree_bouton_simple(1, 2, 8, 2, "Editeur de niveaux", arrondi=0.75)
    boutons.cree_bouton_simple(1, 4, 8, 4, 'Jouer', arrondi=0.75)
    boutons.cree_bouton_simple(1, 6, 8, 6, 'Niveaux', arrondi=0.75)
    boutons.cree_bouton_simple(1, 8, 8, 8, 'Options', arrondi=0.75)
    
    boutons.cree_bouton_booleen(
        9, 9, 9, 9,
        'son', cfg,
        'Son!', 'Muet', arrondi=1, marge_texte=0.8
    )
    boutons.init()
    ev = None
    
    while True:
        try:
            fltk.efface_tout()
            graphiques.background("#3f3e47")
            #boutons.grille.draw()
            boutons.dessiner_boutons(ev)

            ev = fltk.attend_ev()
            tev = fltk.type_ev(ev)
            click = boutons.nom_clic(ev)

            if tev == 'Quitte':
                fltk.ferme_fenetre()
                exit()

            elif tev == "Touche":
                print(fltk.touche(ev))

            elif tev == "ClicGauche":
                # On propose au joueur de reprendre
                if click in {'Jouer', 'Niveaux'}:
                    plateau = None
                    try:
                        if sauvegarde.est_valide():
                            plateau = sauvegarde.menu()
                            if plateau is not None:
                                jeu(plateau)
                                continue
                    except FileNotFoundError:
                        print("La map associée à la sauvegarde n'existe plus",
                             "veuillez sélectionner une autre map")

                if click == 'Jouer':
                    son.sound('MenuOk')
                    try:
                        plateau = Plateau(cfg.carte, duree_anime=0.15)
                        jeu(plateau)
                        son.song("Wait")
                    except FileNotFoundError:
                        print("La map demandée n'existe pas")
                        pass
                    except FichierInvalide:
                        print("Le format de la map est incorrect")
                        pass

                elif click == "Niveaux":
                    son.sound('Menubeep')
                    selecteur.menu()
                    cfg.maj()

                elif click == "Editeur de niveaux":
                    son.sound('Menubeep')
                    editeur.debut()

                elif click == 'son':
                    son.toggle_sound()

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()
