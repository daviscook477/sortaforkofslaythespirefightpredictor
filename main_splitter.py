import argparse
import logging
import json
import os
from pathlib import Path, PosixPath

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M', filemode='w+')
logger = logging.getLogger('main')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--run-directory', default=r'C:\Users\davis\Documents\Slay the Spire Data', help='File path to directory of run log files')
    parser.add_argument('-o', '--output-directory', default=r'C:\Users\davis\Documents\Slay the Spire Runs', help='File path to directory where individual runs are output')
    args = parser.parse_args()

    # Where StS combined run logs are stored as '.json' files
    run_directory = args.run_directory
    output_directory = args.output_directory

    run_globs = [path for path in Path(run_directory).glob('**/*.json')]
    run_files = []
    for glob in run_globs:
        if (os.path.isfile(glob)):
            run_files.append(glob)

    index = 0

    for run_file in run_files:
        with run_file.open() as fin:
            run_datas = json.load(fin)
            for run_data in run_datas:
                output_file = os.path.join(output_directory, f'{index}.run')
                with open(output_file, 'w') as fout:
                    json.dump(run_data['event'], fout)
                index += 1

if __name__ == "__main__":
    main()
