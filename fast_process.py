import datetime
import json
import logging
import re
import sys
from datetime import date
from itertools import chain
from multiprocessing import Pool, Manager
from pathlib import Path, PosixPath
from typing import List, Tuple

from tqdm import tqdm

from common import InvalidRunError, StSGlobals
from run import Run

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M', filemode='w+')
logger = logging.getLogger('main')

class FastProcess:
    """
    Process all of the Slay the Spire run data in a directory.
    """

    def __init__(self, data_directory: str, num_processes: int):
        """
        Go through a directory and split the files amongst processes
        """
        self.data_directory = data_directory
        self.num_processes = num_processes
        self.run_list = self.get_file_list()

    def get_file_list(self):
        data_globs = [path for path in Path(self.data_directory).glob('**/*.json')]
        data_files = []
        for glob in data_globs:
            if (os.path.isfile(glob)):
                data_files.append(glob)
        return data_files