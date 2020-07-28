import os
import sys
import pytest
import requests

ROOTDIR = os.path.dirname(
    os.path.dirname(
    os.path.dirname(__file__)))

sys.path = [ROOTDIR] + sys.path

from runTracker.src import webscraper as wscr
from runTracker.src import settings
from runTracker.src import credentials

assert ROOTDIR in wscr.__file__
assert ROOTDIR in settings.__file__
assert ROOTDIR in credentials.__file__


@pytest.fixture(scope='module')
def webscraper():
    webscraper = wscr.WebScraper()
    
    return webscraper

def test_can_create_webscraper(webscraper):
    assert isinstance(webscraper, wscr.WebScraper)

def test_web_scraper_has_login_url(webscraper):
    assert hasattr(webscraper, 'login_url')

def test_login_url_matches_settings_url(webscraper):
    assert webscraper.login_url == settings.LOGIN_URL

def test_web_scraper_has_workout_url(webscraper):
    assert hasattr(webscraper, 'workout_url')

def test_workout_url_matches_settings_url(webscraper):
    assert webscraper.workout_url == settings.WORKOUT_URL

def test_webscraper_has_attr_credentials(webscraper):
    assert hasattr(webscraper, 'credentials')

def test_webscraper_credentials_match_cred_module(webscraper):
    assert webscraper.credentials == credentials.USER_CREDENTIALS

def test_webscraper_has_session_attr(webscraper):
    assert hasattr(webscraper, 'session')

def test_session_attr_is_none(webscraper):
    assert webscraper.session is None

def test_session_can_be_created(webscraper):
    webscraper.create_session()
    assert isinstance(webscraper.session, requests.sessions.Session)

def test_session_can_log_in_to_maymyrun(webscraper):
    webscraper.create_session()
    request = webscraper.login()
    assert request.status_code == requests.codes.ok

def test_bad_login_data_returns_error():
    webscraper = wscr.WebScraper()
    webscraper.create_session()
    webscraper.credentials = {'username':'test@test.com', 
        'password':'test'}
    with pytest.raises(AssertionError):
        webscraper.login()

def test_bad_url_returns_error():
    webscraper = wscr.WebScraper()
    webscraper.create_session()
    webscraper.login_url = None
    with pytest.raises(Exception):
        webscraper.login()

def test_webscraper_has_raw_data_attr(webscraper):
    assert hasattr(webscraper, 'raw_data')

def test_webscraper_raw_data_is_empty_dict(webscraper):
    assert isinstance(webscraper.raw_data, dict)
    assert not len(webscraper.raw_data)

def test_webscraper_can_connect_to_workout_url(webscraper):
    webscraper.create_session()
    webscraper.login()
    request = webscraper.create_request(year=2019, month=11)
    assert request.status_code == requests.codes.ok

def test_webscraper_gets_workout_data(webscraper):
    webscraper.create_session()
    webscraper.login()
    monthly_data = webscraper.request_data(year=2019, month=11)
    assert len(monthly_data) == 12

def test_run_web_scraper(webscraper):
    webscraper.run_web_scraper()
    assert webscraper.session is None
    assert len(webscraper.raw_data)



