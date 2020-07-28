import os
import sys
import json
import datetime

ROOTDIR = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__)))

sys.path = [ROOTDIR] + sys.path

from runTracker.src import settings
from runTracker.src import runobject
from runTracker.mocks import mockdata

CACHE_LOCATION = os.path.join(
    os.path.dirname(__file__), '../data/cacheddata.json')
INITIAL_IDX = 0


class RunTracker():
    def __init__(self, use_mocks, **kwargs):
        self.use_mocks = use_mocks

        self.scraper = kwargs.get('scraper')
        self.client = kwargs.get('client')
        self.dconverter = kwargs.get('dconverter')
        self.ddisplayer = kwargs.get('ddisplayer')

        self.use_cache = True
        self.cache_date = None
        self.cache = self.read_cache()

        self.raw_data = None
        self.processed_data = None
        self.runs = []

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self, cache_value):
        self._cache = cache_value

        if not cache_value:
            self.use_cache = False
            return

        today = datetime.date.today()
        cache_date = get_cache_date(cache_value=cache_value)

        if today > cache_date:
            self.use_cache = False 
        
        self.cache_date = str(cache_date)

    def read_cache(self):
        if not os.path.exists(CACHE_LOCATION):
            return None

        with open(CACHE_LOCATION) as json_file:
            try:
                cached_data = json.load(json_file)
            except json.decoder.JSONDecodeError:
                return None

        return cached_data

    def save_cache(self, data):
        cache_data = {}
        cache_data[datetime.date.today().strftime('%Y-%m-%d')] = data
        with open(CACHE_LOCATION, 'w+') as json_file:
            json.dump(cache_data, json_file, indent=4)

    def run_runtracker(self):
        self.gather_run_data()

        if not self.raw_data:
            return

        self.process_run_data()

        if not self.runs:
            return

        self.visualise_run_data()

    def gather_run_data(self):
        if self.use_mocks:
            self.raw_data = mockdata.mockdata
            return

        if self.use_cache:
            print('Using Cached Data')
            self.raw_data = self.cache[self.cache_date]
        else:
            print('Gathering Fresh Data')
            self.scraper.run_web_scraper()
            self.raw_data = self.scraper.raw_data
            self.save_cache(data=self.raw_data)

    def process_run_data(self):
        self.processed_data = self.client.process_rundata(self.raw_data)

        for run_data in self.processed_data:
            run = runobject.Run(**run_data)
            self.runs.append(run)

    def visualise_run_data(self):
        converted_data = self.dconverter.convert_data(rundata=self.runs)
        self.ddisplayer.display_data(rundata=converted_data, datatype='pace')


def get_cache_date(cache_value):
    cache_date = list(cache_value.keys())[INITIAL_IDX]
    year, month, day  = tuple(
        map(int, cache_date.split(settings.DATE_DELIMITTER)))
    processed_cache_date = datetime.date(year, month, day)

    return processed_cache_date
