"""
Projet 2 : Ricosheep

Amal ABDALLAH
Nicolas SEBAN
Adam SOUIOU
"""

from bouton import Boutons
from plateau import Plateau, FichierInvalide
from ricosheep import boutons_jeu_init, jeu
from os import path
import randomizer
import animation
import graphiques
import cfg
import fltk
import selecteur
import sauvegarde
import editeur
import son


invite_reprendre = {'Jouer', 'Niveaux', "100% Aléatoire", "Aléatoire contrôlé"}
duree_anime = 0.2


def menu():
    son.song("Wait")
    boutons = Boutons((20, 20))
    logo = graphiques.image_grille(
        2, 0, 17, 5,
        path.join('media', 'images', 'Logo_ricosheep.png'), boutons.grille)
    boutons.cree_bouton_simple(3, 6, 16, 7, 'Jouer',
                               arrondi=0.75)
    boutons.cree_bouton_simple(3, 9, 16, 10, 'Niveaux',
                               arrondi=0.75)
    boutons.cree_bouton_simple(3, 12, 16, 13, "Editeur de niveaux",
                               arrondi=0.75)
    boutons.cree_bouton_simple(3, 15, 9, 16, "100% Aléatoire",
                               arrondi=0.75)
    boutons.cree_bouton_simple(10, 15, 16, 16, 'Aléatoire contrôlé',
                               arrondi=0.75)

    boutons.cree_bouton_booleen(
        18, 18, 19, 19,
        'son', cfg, '🔊', '🔇', arrondi=1, marge_texte=0.8, icone=True
    )
    boutons.cree_bouton_booleen(
        15, 18, 16, 19,
        'animation', cfg, '🐑', '🚫', arrondi=1, marge_texte=0.8, icone=True
    )
    plateau_pos = (0, 0, 15, 22)

    boutons.init()

    ev = None
    liste_chute = animation.initialisation(12)

    while True:
        try:
            fltk.efface_tout()
            graphiques.background("#3f3e47")
            if cfg.animation:
                animation.dessiner(liste_chute)
            boutons.dessiner_boutons(ev)
            fltk.afficher_image(
                logo.centre_x, logo.centre_y,
                logo.image, 'center'
            )

            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)
            click = boutons.nom_clic(ev)

            if tev == 'Quitte':
                return

            elif tev == "ClicGauche":
                # On propose au joueur de reprendre
                if click in invite_reprendre:
                    plateau = None
                    try:
                        if sauvegarde.est_valide():
                            plateau, boutons_jeu = sauvegarde.menu()
                            if plateau is not None:
                                jeu(plateau, boutons_jeu)
                                continue
                    except FileNotFoundError:
                        print("La map associée à la sauvegarde n'existe plus",
                              "veuillez sélectionner une autre map")

                if click == 'Jouer':
                    son.sound('MenuAccept')
                    try:
                        boutons_jeu = boutons_jeu_init()
                        plateau = Plateau(
                            cfg.carte,
                            duree_anime=duree_anime,
                            grille_base=boutons_jeu.grille,
                            grille_pos=plateau_pos,
                        )
                        son.song("Otherside")
                        jeu(plateau, boutons_jeu)
                    except FileNotFoundError:
                        print("La map demandée n'existe pas")
                        pass
                    except FichierInvalide:
                        print("Le format de la map est incorrect")
                        pass

                elif click == "Niveaux":
                    son.sound('MenuBleep')
                    selecteur.menu()
                    cfg.maj()

                elif click == "Editeur de niveaux":
                    son.sound('MenuBleep')
                    editeur.debut()

                elif click == "100% Aléatoire":
                    son.sound('MenuAccept')
                    carte = randomizer.generation100()
                    boutons_jeu = boutons_jeu_init()
                    plateau = Plateau(carte,
                                      duree_anime=duree_anime,
                                      grille_base=boutons_jeu.grille,
                                      grille_pos=plateau_pos)
                    jeu(plateau, boutons_jeu)

                elif click == "Aléatoire contrôlé":
                    son.sound('MenuAccept')
                    plateau = randomizer.menu_control()
                    if plateau is None:
                        continue
                    boutons_jeu = boutons_jeu_init()
                    plateau.gen_grille(
                        duree_anime=duree_anime,
                        grille_base=boutons_jeu.grille,
                        grille_pos=plateau_pos)
                    jeu(plateau, boutons_jeu)

                elif click == 'son':
                    son.toggle_sound()

                elif click == 'animation':
                    cfg.toggle_sound_anim('animation')

            fltk.mise_a_jour()

        except KeyboardInterrupt:
            return
