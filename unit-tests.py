import unittest
import solveur
from os import path
from sys import setrecursionlimit
from glob import glob
from plateau import Plateau
setrecursionlimit(10**6)

join = lambda l : path.join(*l)

maps_impossibles = set(
    map(join,
        [ ['maps', 'custom', '1.txt'] ]
    )
)

class TestSolveur(unittest.TestCase):
    
    def testSolveurCorrect(self):
        nb_tests = 0
        for map_file in glob('maps/*/*.txt'):
            if '__' in map_file: continue
            with self.subTest():
                print(f"Test avec {map_file}...")
                plateau = Plateau(map_file, test_mode=True, duree_anime=0)
                back = solveur.tri_copy(plateau.troupeau)
                
                chemin, _ = solveur.profondeur(plateau)
                
                if map_file in maps_impossibles:
                    self.assertTrue(
                        chemin is None,
                        f"Le solveur à renvoyé autre chose\
                        que None, alors que la map est insolvable, \
                        la map était {map_file}")
                    continue
                else:
                    self.assertTrue(
                        chemin is not None,
                        f"Le chemin est None! la map était {map_file}")
                
                solveur.restore(plateau.troupeau, back)
                
                self.assertTrue(solveur.test(chemin, plateau, unittest=True) is True,
                    f"Le chemin n'est pas correct, la map était {map_file}")
            nb_tests += 1
        print(f"{nb_tests} tests ont été réalisés")


if __name__ == '__main__':
    unittest.main()