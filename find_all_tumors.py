import argparse
import csv
import glob
import os
import sys
from pathlib import Path

from CancerDetector import CancerDetector
from TumorReader import TumorReader
from find_tumor import ExitStatus


def process_all_files(dir, output):
    path = os.path.abspath(dir)
    output_file = os.path.abspath(output)
    Path(output_file).touch()
    files = glob.glob(f"{path}/*.in")
    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Filename', 'HasTumor', 'Rows', 'Columns'])
        for file in files:
            try:
                basepath = os.path.basename(file)
                reader = TumorReader(file)
                matrix = reader.read_file()
                detector = CancerDetector(matrix)
                cancer_locations = detector.get_cancer_cells_positions()
                errors = detector.has_errors
            except Exception as e:
                errors = True
            if errors:
                writer.writerow([basepath, "Error", "NA", "NA"])
            elif not len(cancer_locations):
                writer.writerow([basepath, "False", reader.total_rows, detector.total_columns])
            else:
                writer.writerow([basepath, "True", reader.total_rows, detector.total_columns])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Pass in a directory and '
                    'it will find if scan the directory and output a csv file.')
    parser.add_argument('--inputdir', help='the input directory location you want to parse')
    parser.add_argument('--outputfile', help='the output file you want to write to')
    args = parser.parse_args()
    if not args.inputdir:
        raise RuntimeError("You must pass in a directory")
    if not args.outputfile:
        raise RuntimeError("You must pass in a file output")
    process_all_files(args.inputdir, args.outputfile)
