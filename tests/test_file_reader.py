import os
import unittest

from TumorReader import TumorReader


class TestFileReader(unittest.TestCase):
    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        no_tumors_path = os.path.abspath(f"{self.dir_path}/../files/no_tumor.in")
        self.no_tumors_reader = TumorReader(no_tumors_path)
        has_tumors_path = os.path.abspath(f"{self.dir_path}/../files/yes_tumor.in")
        self.has_tumors_reader = TumorReader(has_tumors_path)

    def testCanReadFile(self):
        matrix = self.no_tumors_reader.read_file()
        assert (len(matrix[0]) == 80)

    def testWillThrowErrorOnInvalidFilePath(self):
        bad_path = os.path.abspath(f"{self.dir_path}/../files/foo.in")
        bad_reader = TumorReader(bad_path)
        try:
            bad_reader.read_file()
        except (FileNotFoundError, IOError) as e:
            assert isinstance(e, Exception)
        assert bad_reader.has_error is True

    def testWillReportNoErrorOnInputWithMatchingColumnSize(self):
        self.no_tumors_reader.read_file()
        assert self.no_tumors_reader.has_error is False

    def testWillReportErrorOnInputWithoutMatchingColumnSize(self):
        bad_path = os.path.abspath(f"{self.dir_path}/../files/bad_input.in")
        bad_reader = TumorReader(bad_path)
        try:
            bad_reader.read_file()
        except ValueError as e:
            assert isinstance(e, ValueError)
        assert bad_reader.has_error is True

    def testWillReportErrorOnInputWithEmptyLine(self):
        path = os.path.abspath(f"{self.dir_path}/../files/empty_line_input.in")
        bad_reader = TumorReader(path)
        try:
            bad_reader.read_file()
        except ValueError as e:
            assert isinstance(e, ValueError)
        assert bad_reader.has_error is True

    def testWillIgnoreInvalidCharacters(self):
        path = os.path.abspath(f"{self.dir_path}/../files/ignore_non_alpha_characters.in")
        reader = TumorReader(path)
        matrix = reader.read_file()
        assert (len(matrix[0]) == 80)


if __name__ == '__main__':
    unittest.main()
