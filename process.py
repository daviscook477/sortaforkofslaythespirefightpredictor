import datetime
import json
import logging
import re
import sys
import os
from datetime import date
from itertools import chain
from multiprocessing import Pool, Manager
from pathlib import Path, PosixPath
from typing import List, Tuple
from json import JSONDecodeError

from tqdm import tqdm

from common import InvalidRunError, StSGlobals
from run import Run

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M', filemode='w+')
logger = logging.getLogger('main')

class Process:
    """
    Used to process a directory's worth of Slay the Spire run files.
    """

    def __init__(self, run_directory: str, num_processes: int):
        """
        Go through a directory of runs and process them all in batches
        """
        self.run_directory = run_directory
        self.num_processes = num_processes
        self.run_list = self.get_file_list()
        self.logs = self.get_logs()
        self.date = date.today()

    def get_file_list(self):
        run_globs = [path for path in Path(self.run_directory).glob('**/*.json')]
        run_files = []
        for glob in run_globs:
            if (os.path.isfile(glob)):
                run_files.append(glob)
        return run_files

    def get_logs(self):
        """
        Keep track of these counts in each process
        """
        logs = Manager().dict()
        logs['file_not_opened'] = 0
        logs['bad_file_count'] = 0
        logs['total_file_count'] = len(self.run_list)
        logs['file_not_processed_count'] = 0
        logs['file_processed_count'] = 0
        logs['file_master_not_match_count'] = 0
        logs['invalid_runs_found'] = 0
        logs['num_fights'] = 0
        return logs

    def process_runs(self):
        # Break up files for each process
        run_chunks = self.chunks(self.run_list, self.num_processes)

        output_dir = Path(f'C:/Users/davis/Documents/Slay the Spire Runs/{self.date}')
        output_dir.mkdir(exist_ok=True, parents=True)

        logger.info(f'Starting {self.num_processes} processes')
        with Pool(processes=self.num_processes) as p:
            chain(*p.imap(self.process_chunk, [(run_chunk, i, output_dir)
                                               for i, run_chunk in enumerate(run_chunks)]))

        logger.info(
            f'Files not able to open: {self.logs["file_not_opened"]} => {((self.logs["file_not_opened"] / self.logs["total_file_count"]) * 100):.1f} %')
        logger.info(
            f'Files filtered with pre-filter: {self.logs["bad_file_count"]} => {((self.logs["bad_file_count"] / self.logs["total_file_count"]) * 100):.1f} %')
        logger.info(
            f'Invalid run files: {self.logs["invalid_runs_found"]} => {((self.logs["invalid_runs_found"] / self.logs["total_file_count"]) * 100):.1f} %')
        logger.info(
            f'Files SUCCESSFULLY processed: {self.logs["file_processed_count"]} => {((self.logs["file_processed_count"] / self.logs["total_file_count"]) * 100):.1f} %')
        logger.info(
            f'Files with master deck not matching created deck: {self.logs["file_master_not_match_count"]} => {((self.logs["file_master_not_match_count"] / self.logs["total_file_count"]) * 100):.1f} %')
        logger.info(
            f'Files not processed: {self.logs["file_not_processed_count"]} => {((self.logs["file_not_processed_count"] / self.logs["total_file_count"]) * 100):.1f} %')
        logger.info(f'Total files: {self.logs["total_file_count"]}')
        logger.info(f'Number of usable examples: {self.logs["num_fights"]}')

    @staticmethod
    def chunks(long_list: List, num_chunks: int):
        """
        Yield num_chunks number of chunks from long_list.
        """
        for i in range(num_chunks):
            yield long_list[i::num_chunks]

    def process_chunk(self, input_data: Tuple[List, int, PosixPath], batch_size: int = 1000):
        chunk, process_id, output_dir = input_data
        processed_runs = []
        batch_count = 0
        for run_path in tqdm(chunk):
            try:
                runs = self.load_run(run_path)
            except JSONDecodeError:
                continue
            for run in runs:
                run = run['event']
                if self.is_bad_file(run):
                    self.logs['bad_file_count'] += 1
                else:
                    try:
                        processed_runs.append(Run(run).process_run())
                        self.logs['file_processed_count'] += 1
                    # Just pass all the exceptions we know about
                    except InvalidRunError:
                        self.logs['invalid_runs_found'] += 1
                        continue
                    except RuntimeError as e:
                        self.logs['file_master_not_match_count'] += 1
                        logger.debug(f'{run_path}\n')
                        continue
                    except IndexError as e:
                        self.logs['invalid_runs_found'] += 1
                        continue
                    except KeyError as e:
                        self.logs['invalid_runs_found'] += 1

                if len(processed_runs) > batch_size:
                    logger.info('Saving batch')
                    self.write_file(processed_runs, f'{output_dir}/data_{self.date}_{process_id}_{batch_count}.json')
                    logger.info(f'Wrote batch {batch_count} for process {process_id} of size {batch_size} to file')
                    processed_runs = []
                    batch_count += 1

        self.write_file(processed_runs, f'{output_dir}/data_{self.date}_{process_id}.json')
        print(self.logs)

    def write_file(self, data, name):
        with open(name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    def load_run(self, run_path):
        with run_path.open() as file:
            data = json.load(file)
        return data

    def is_bad_file(self, run):
        # Corrupted files
        necessary_fields = {'damage_taken', 'event_choices', 'card_choices', 'relics_obtained', 'campfire_choices',
                            'items_purchased', 'item_purchase_floors', 'items_purged', 'items_purged_floors',
                            'character_chosen', 'boss_relics', 'floor_reached', 'master_deck', 'relics'}
        present_fields = set(run.keys())
        has_necessary_fields = necessary_fields.issubset(present_fields)
        if not has_necessary_fields:
            logger.debug('Does not have necessary fields')
            return True

        # Modded games
        key = 'character_chosen'
        if run.get(key) not in StSGlobals.BASE_GAME_CHARACTERS:
            logger.debug('Does not have base game character')
            return True

        key = 'master_deck'
        if set(run.get(key, {'Empty Set'})).issubset(StSGlobals.BASE_GAME_CARDS_AND_UPGRADES) is False:
            logger.debug('Does not use base game deck')
            return True

        key = 'relics'
        if set(run.get(key, {'Empty Set'})).issubset(StSGlobals.BASE_GAME_RELICS) is False:
            logger.debug('Does not have base game relics')
            return True

        key = 'ReplayTheSpireMod:Calculation Training+1'
        if key in run['master_deck']:
            logger.debug('Uses ReplayTheSpireMod')
            return True

        # Watcher files since full release of watcher (v2.0) and ironclad, silent, defect since v1.0
        key = 'build_version'
        if key not in run or self.valid_build_number(run[key], run['character_chosen']) is False:
            logger.debug('Invalid build number')
            return True

        # Non standard runs
        key = 'is_trial'
        if run.get(key, True):
            logger.debug('Trial run')
            return True

        key = 'is_daily'
        if run.get(key, True):
            logger.debug('Daily run')
            return True

        key = 'daily_mods'
        if key in run:
            logger.debug('Daily run')
            return True

        key = 'chose_seed'
        if run.get(key, True):
            logger.debug('Chose seed')
            return True

        # Endless mode
        key = 'is_endless'
        if run.get(key, True):
            logger.debug('Endless mode')
            return True

        key = 'circlet_count'
        if run.get(key, 1) > 0:
            return True

        key = 'floor_reached'
        if run.get(key, 61) > 60:
            logger.debug('More floors than possible')
            return True

        # Really bad players or give ups
        key = 'floor_reached'
        if run.get(key, 1) < 4:
            logger.debug('Player stinks')
            return True

        key = 'score'
        if run.get(key, 1) < 10:
            logger.debug('Player stinks')
            return True

        key = 'player_experience'
        if run.get(key, 1) < 10:
            logger.debug('Player stinks')
            return True

        # low ascension level
        key = 'ascension_level'
        if run.get(key, 1) < 15:
            logger.debug('Low ascension')
            return True

        # losses
        key = 'floor_reached'
        if run.get(key, 1) < 50:
            logger.debug('Lost run')
            return True

    def valid_build_number(self, string, character):
        pattern = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}$')
        if pattern.match(string):
            m = re.search('(.+)-(.+)-(.+)', string)
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))

            date = datetime.date(year, month, day)
            if date >= datetime.date(2020, 1, 16):
                return True
            elif character in ['IRONCLAD', 'THE_SILENT', 'DEFECT'] and date >= datetime.date(2019, 1, 23):
                return True

        return False
