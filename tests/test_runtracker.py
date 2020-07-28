import os
import sys
import pytest

ROOTDIR = os.path.dirname(
    os.path.dirname(
    os.path.dirname(__file__)))

sys.path = [ROOTDIR] + sys.path

from runTracker.src import runtracker as rt
from runTracker.src import rundataclient as rdc
from runTracker.src import runobject as runobj

assert ROOTDIR in rt.__file__
assert ROOTDIR in rdc.__file__
assert ROOTDIR in runobj.__file__

@pytest.fixture(scope='module')
def rtracker():
    client = rdc.Client()
    rtracker = rt.RunTracker(use_mocks=True, client=client)
    return rtracker

@pytest.fixture(scope='module')
def runs(rtracker):
    rtracker.gather_run_data()
    rtracker.process_run_data()

    return rtracker.runs

def test_run_tracker_class_creation(rtracker):
    assert isinstance(rtracker, rt.RunTracker)

def test_run_tracker_has_run_runtracker_fn(rtracker):
    assert 'run_runtracker' in [func for func in dir(rtracker)
        if callable(getattr(rtracker, func))]

def test_run_tracker_has_gather_data_fn(rtracker):
    assert 'gather_run_data' in [func for func in dir(rtracker)
        if callable(getattr(rtracker, func))]

def test_run_tracker_has_process_data_fn(rtracker):
    assert 'process_run_data' in [func for func in dir(rtracker)
        if callable(getattr(rtracker, func))]

def test_run_tracker_has_visualise_data_fn(rtracker):
    assert 'visualise_run_data' in [func for func in dir(rtracker)
        if callable(getattr(rtracker, func))]

def test_run_tracker_has_use_mocks_attr(rtracker):
    assert hasattr(rtracker, 'use_mocks')

def test_run_tracker_needs_use_mocks_attr():
    with pytest.raises(TypeError):
        rtracker = rt.RunTracker()

def test_run_tracker_has_scraper_attr(rtracker):
    assert hasattr(rtracker, 'scraper')

def test_run_tracker_has_client_attr(rtracker):
    assert hasattr(rtracker, 'client')

def test_run_tracker_has_rawdata_attr(rtracker):
    assert hasattr(rtracker, 'raw_data')

def test_run_tracker_has_processed_data_attr(rtracker):
    assert hasattr(rtracker, 'processed_data')

def test_run_tracker_has_runs_attr(rtracker):
    assert hasattr(rtracker, 'runs')

def test_gather_run_data_returns_dict(rtracker):
    rtracker.gather_run_data()
    assert isinstance(rtracker.raw_data, dict)

def test_gather_run_data_returns_populated_dict(rtracker):
    rtracker.gather_run_data()
    assert len(rtracker.raw_data) == 11

def test_process_run_data_returns_populated_dict(rtracker):
    rtracker.gather_run_data()
    rtracker.process_run_data()
    assert len(rtracker.processed_data) == 9

def test_runs_are_run_objects(runs):
    assert all([isinstance(run, runobj.Run) for run in runs])

def test_run_class_has_original_distance_attr(runs):
    assert all([hasattr(run, 'original_distance') for run in runs])

def test_run_class_has_pace_attr(runs):
    assert all([hasattr(run, 'adjusted_pace') for run in runs])

def test_run_class_has_speed_attr(runs):
    assert all([hasattr(run, 'adjusted_speed') for run in runs])
