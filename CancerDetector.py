from typing import Generator


class CancerDetector(object):
    CURRENT_VALUE = 'current_value'
    TOUCHING = 'touching'
    POS = 'pos'
    has_errors = False
    first_detected = None
    file_line = None
    total_rows = 0
    total_columns = 0

    def __init__(self, matrix_array: list) -> None:
        super().__init__()
        self.matrix_array = matrix_array

    def neighboring(self, array: list) -> Generator:
        total_rows, current_row_size = len(array), len(array[0])
        self.total_rows = total_rows
        self.total_columns = current_row_size  # So long as this is not a jagged array, this is valid
        offset = (0, -1, 1)
        indices = (
            (i, j) for i in range(total_rows)
            for j in range(current_row_size)
        )
        for i, j in indices:
            all_neigh = ((i + x, j + y) for x in offset for y in offset)
            valid = (
                (i, j) for i, j in all_neigh if
                (0 <= i < total_rows) and (0 <= j < current_row_size)
            )
            yield next(valid), valid

    def get_neighboring_elements(
            self,
            current_row: int,
            current_column: int,
            item
    ) -> dict:
        values = dict()
        try:
            current_item = self.matrix_array[current_row][current_column]
            values[self.POS] = (current_row, current_column)
            values[self.CURRENT_VALUE] = current_item
            values[self.TOUCHING] = [self.matrix_array[x][y] for x, y in item]
        except (IndexError, ValueError) as e:
            self.has_errors = True
        return values

    @staticmethod
    def has_cancer(results: dict) -> bool:
        current_value = results.get(CancerDetector.CURRENT_VALUE)
        touching = results.get(CancerDetector.TOUCHING)
        if not current_value or not touching:
            return False
        return current_value not in touching

    def get_neighboring_cells(self) -> list:
        neighbors = []
        for (current_row, current_column), generator in self.neighboring(self.matrix_array):
            els = self.get_neighboring_elements(
                current_row,
                current_column,
                generator
            )
            if els.get('touching', None):
                neighbors.append(els)
        return neighbors

    def get_cancer_cells_positions(self) -> set:
        cancer_positions = []
        cancer_values = []
        neighboring_cells = self.get_neighboring_cells()
        for cell in neighboring_cells:
            if self.has_cancer(cell):
                pos = cell.get(self.POS)
                self.first_detected = cell
                self.file_line = (pos[0] + 1, pos[1] + 1)
                cancer_values.append(cell.get(self.CURRENT_VALUE))
        if len(cancer_values):
            cancer_values = set(cancer_values)
            for cell in neighboring_cells:
                if cell.get(self.CURRENT_VALUE) in cancer_values:
                    cancer_positions.append(cell.get(self.POS))

        return set(cancer_positions)
