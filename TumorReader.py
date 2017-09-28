import os
from typing import IO


class TumorReader(object):
    has_error = False
    error_message = None
    total_rows = 0
    total_columns = 0

    def __init__(self, file_name: str) -> None:
        if not len(file_name):
            self.has_error = True
            raise FileNotFoundError("Must pass in a file name to read")
        self.file_name = file_name

    def read_file(self):
        try:
            with open(self.file_name, 'r') as file:
                lines = self.get_list_from_file(file)
            return lines
        except IOError as e:
            self.raise_io_error(e)
        except FileExistsError as e:
            self.raise_file_exists_error(e)

    def get_list_from_file(self, file: IO) -> list:
        full_lines = []
        line_count = 0
        previous_len = None
        total_lines = file.read().strip().split(os.linesep)
        for line in total_lines:
            lines = []
            line_count += 1
            clean_line = self.convert_to_lowercase_alphas(line)
            current_len = len(clean_line)
            if not current_len:
                self.has_error = True
            if previous_len is None:
                previous_len = current_len
            elif previous_len != current_len:
                self.has_error = True
                self.error_message = f"Previous line does not match current line on line: {line_count}"
                raise ValueError(self.error_message)
            else:
                previous_len = current_len
            if current_len:
                for character in clean_line:
                    lines.append(character)
            full_lines.append(lines)
        self.total_rows = len(full_lines)
        self.total_columns = current_len
        return full_lines

    def raise_file_exists_error(self, e):
        self.has_error = True
        self.error_message = f"File {self.file_name} already exists"
        raise e

    def raise_io_error(self, e):
        self.has_error = True
        self.error_message = f"No file called {self.file_name} exists"
        raise e

    @staticmethod
    def convert_to_lowercase_alphas(string: str) -> str:
        new_str = ''
        for letter in string:
            if not letter.isalpha():
                continue
            new_str += letter.lower()
        return new_str
