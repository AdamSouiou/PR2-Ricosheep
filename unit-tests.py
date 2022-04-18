import unittest
from sys import setrecursionlimit
setrecursionlimit(10**6)
from glob import glob
import solveur
from plateau import Plateau

maps_impossibles = {'maps/square/map1.txt',
                    'maps/custom/1.txt'}

class TestSolveur(unittest.TestCase):
    
    def testSolveurCorrect(self):
        nb_corrects = 0
        for map_file in glob('maps/*/*.txt'):
            if '__' in map_file: continue
            with self.subTest():
                print(map_file)
                plateau = Plateau(map_file, test_mode=True)
                back = solveur.tri_copy(plateau.troupeau)
                
                chemin, _ = solveur.profondeur(plateau)
                
                if map_file in maps_impossibles:
                    self.assertTrue(
                        chemin is None,
                        "Le solveur à renvoyé autre chose\
                        que None, alors que la map est insolvable")
                    continue
                else:
                    self.assertIsNotNone(
                        chemin,
                        f"Pas de solutions!, la map était {map_file}")

                self.assertTrue(
                    chemin is not None,
                    f"Le chemin est None! la map était {map_file}")
                
                solveur.restore(plateau.troupeau, back)
                self.assertTrue(solveur.test(chemin, plateau) is True,
                    f"Le chemin n'est pas correct, la map était {map_file}")
            nb_corrects += 1
        print(nb_corrects)
                

if __name__ == '__main__':
    unittest.main()