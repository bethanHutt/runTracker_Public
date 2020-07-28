import os
import sys
import requests
import datetime

ROOTDIR = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__)))

sys.path = [ROOTDIR] + sys.path

from runTracker.src import settings
from runTracker.src import credentials

assert ROOTDIR in settings.__file__
assert ROOTDIR in credentials.__file__


class WebScraper():
    def __init__(self):
        self.login_url = settings.LOGIN_URL
        self.workout_url = settings.WORKOUT_URL
        self.credentials = credentials.USER_CREDENTIALS
        self.today = datetime.date.today()

        self.session = None
        self.raw_data = {}
        self.dated_data = {}

    def run_web_scraper(self):
        self.create_session()
        self.login()
        self.compile_workout_data()
        self.close_session()

    def create_session(self):
        self.session = requests.Session()

    def login(self):
        request = self.session.post(
            url=self.login_url,
            json=self.credentials)

        assert request.status_code == requests.codes.ok
        return request

    def compile_workout_data(self):
        for year in range(settings.START_YEAR, settings.CURRENT_YEAR):
            for month in range(1, 13):
                monthly_data = self.request_data(year=year, month=month)
                self.raw_data.update(monthly_data)
        self.dated_data[self.today] = self.raw_data

    def create_request(self, year, month):
        request = self.session.get(
            url=self.workout_url.format(month=month, year=year))

        assert request.status_code == requests.codes.ok
        return request

    def request_data(self, year, month):
        request = self.create_request(year=year, month=month)

        monthly_data = (request.json()['workout_data']['workouts'])
        return monthly_data

    def close_session(self):
        self.session.close()
        self.session = None
