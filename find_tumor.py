import argparse
import os
import sys

from exitstatus import ExitStatus

from CancerDetector import CancerDetector
from TumorReader import TumorReader

ExitStatus.unix_failure = -1


def process_file(file):
    try:
        path = os.path.abspath(file)
        reader = TumorReader(path)
        matrix = reader.read_file()
        detector = CancerDetector(matrix)
        cancer_locations = detector.get_cancer_cells_positions()
        errors = detector.has_errors
    except Exception:
        errors = True
    if errors:
        print(f"Error NA NA")
        sys.exit(ExitStatus.unix_failure)
    elif not len(cancer_locations):
        print(f"False {reader.total_rows} {reader.total_columns}")
    else:
        print(f"True {reader.total_rows} {reader.total_columns}")
    sys.exit(ExitStatus.success)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pass in a file and it will find if a tumor is present.')
    parser.add_argument('--inputfile', help='the input file location you want to parse')
    args = parser.parse_args()
    if not args.inputfile:
        raise RuntimeError("You must pass in a file")
    process_file(args.inputfile)
