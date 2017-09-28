import unittest
from CancerDetector import CancerDetector
from TumorReader import TumorReader
import os


class TestCanReadFilesAndDetectCancer(unittest.TestCase):
    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        no_cancer_path = os.path.abspath(f"{self.dir_path}/../files/no_tumor.in")
        self.no_cancer_reader = TumorReader(no_cancer_path)
        cancer_path = os.path.abspath(f"{self.dir_path}/../files/yes_tumor.in")
        self.has_cancer_reader = TumorReader(cancer_path)

    def testWillShowNoCancerIfNotExists(self):
        matrix = self.no_cancer_reader.read_file()
        detector = CancerDetector(matrix)
        cancer_locations = detector.get_cancer_cells_positions()
        assert (len(cancer_locations) == 0)

    def testWillShowCancerIfExists(self):
        matrix = self.has_cancer_reader.read_file()
        detector = CancerDetector(matrix)
        cancer_locations = detector.get_cancer_cells_positions()
        assert len(cancer_locations) == 199


if __name__ == '__main__':
    unittest.main()
