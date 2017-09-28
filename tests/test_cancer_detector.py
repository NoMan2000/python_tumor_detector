import unittest

from CancerDetector import CancerDetector


class CancerDetectorTestCase(unittest.TestCase):
    def setUp(self):
        self.no_cancer = [
            ['A', 'A', 'B', 'B'],
            ['A', 'B', 'B', 'B'],
            ['A', 'C', 'D', 'C'],
            ['C', 'C', 'C', 'D'],
        ]

        self.has_cancer = [
            ['A', 'A', 'B', 'A'],
            ['A', 'B', 'B', 'B'],
            ['A', 'C', 'D', 'C'],
            ['C', 'C', 'C', 'D'],
        ]

        self.no_cancer_detector = CancerDetector(self.no_cancer)
        self.has_cancer_detector = CancerDetector(self.has_cancer)

    def testGetNeighboringCellsWillReturnCorrectCount(self):
        no_cancer_cells = self.no_cancer_detector.get_neighboring_cells()
        has_cancer_cells = self.has_cancer_detector.get_neighboring_cells()
        assert (no_cancer_cells.__len__() == 16)
        assert (has_cancer_cells.__len__() == 16)

    def testGetNeighboringCellsWillShowNeighbors(self):
        no_cancer_cells = self.no_cancer_detector.get_neighboring_cells()
        has_cancer_cells = self.has_cancer_detector.get_neighboring_cells()
        assert (no_cancer_cells[3].get(CancerDetector.TOUCHING) == ['B', 'B', 'B'])
        assert (has_cancer_cells[3].get(CancerDetector.TOUCHING) == ['B', 'B', 'B'])

    def testGetNeighboringCellsWillShowCurrentValue(self):
        no_cancer_cells = self.no_cancer_detector.get_neighboring_cells()
        has_cancer_cells = self.has_cancer_detector.get_neighboring_cells()
        assert (no_cancer_cells[3].get(CancerDetector.CURRENT_VALUE) == 'B')
        assert (has_cancer_cells[3].get(CancerDetector.CURRENT_VALUE) == 'A')

    def testWillFindNoCancerCellsWhenNotPresent(self):
        no_cancer_cells = self.no_cancer_detector.get_cancer_cells_positions()
        assert (len(no_cancer_cells) == 0)

    def testWillFindCancerCellsWhenPresent(self):
        has_cancer_cells = self.has_cancer_detector.get_cancer_cells_positions()
        assert (len(has_cancer_cells) == 5)
        new_set = {(0, 0), (0, 1), (0, 3), (1, 0), (2, 0)}
        assert (new_set == has_cancer_cells)


if __name__ == '__main__':
    unittest.main()
