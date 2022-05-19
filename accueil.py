from bouton import Boutons
from plateau import Plateau
import animation
import graphiques
import cfg
import fltk
import selecteur
import sauvegarde
import editeur
import son


def menu():
    logo = graphiques.logo()
    boutons = Boutons((20,20))
    boutons.cree_bouton_simple(3, 6, 16, 7, "Editeur de Niveaux", arrondi = 0.75)
    boutons.cree_bouton_simple(3, 9, 16, 10, 'Jouer', arrondi=0.75)
    boutons.cree_bouton_simple(3, 12, 16, 13, 'Niveaux', arrondi=0.75)
    boutons.cree_bouton_simple(3, 15, 16, 16, 'Options', arrondi=0.75)
    
    boutons.cree_bouton_booleen(
        18, 18, 19, 19,
        'son', cfg,
        'Son!', 'Muet', arrondi=1, marge_texte=0.8
    )
    boutons.cree_bouton_booleen(
        15, 18, 16, 19,
        'animation', cfg,
        'Anim !', 'Beeeh', arrondi=1, marge_texte=0.8
    )
    boutons.init()

    # fltk.efface_tout()
    ev = None

    liste_chute = animation.initialisation(12)

    while True:
        try:
            fltk.efface_tout()
            graphiques.background("#3f3e47")
            if cfg.animation: animation.dessiner(liste_chute)
            #boutons.grille.draw()
            boutons.dessiner_boutons(ev)
            fltk.afficher_image(cfg.largeur_fenetre/2, cfg.hauteur_fenetre*0.15, logo, 'center')

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)

            if tev == 'Quitte':
                fltk.ferme_fenetre()
                exit()

            click = boutons.nom_clic(ev)

            if tev == "Touche":
                print(fltk.touche(ev))

            elif tev == "ClicGauche":
                if click in {'Jouer', 'Niveaux', 'Editeur de Niveaux'}:
                    plateau = None
                    if sauvegarde.est_valide():
                        plateau = sauvegarde.menu()

                    if click == "Jouer":
                        son.sound('MenuOk')
                        return plateau or Plateau(cfg.carte, duree_anime=0.2)
                    elif click == "Niveaux":
                        son.sound('Menubeep')
                        selecteur.menu()
                        cfg.maj()
                    elif click == "Editeur de Niveaux":
                        son.sound('Menubeep')
                        editeur.debut()
                elif click == 'son':
                    son.toggle_sound()

                elif click == 'animation':
                    cfg.toggle_sound_anim('animation')



            fltk.mise_a_jour()

        except KeyboardInterrupt:
            exit()
