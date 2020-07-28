import os
import sys
import pytest

ROOTDIR = os.path.dirname(
    os.path.dirname(
    os.path.dirname(__file__)))

sys.path = [ROOTDIR] + sys.path

from runTracker.src import rundataclient as rdc
from runTracker.src import rundatahandler as hdlr
from runTracker.src import settings
from runTracker.mocks import mockdata as mock

assert ROOTDIR in rdc.__file__
assert ROOTDIR in hdlr.__file__
assert ROOTDIR in settings.__file__
assert ROOTDIR in mock.__file__


@pytest.fixture(scope='module')
def client():
    client = rdc.Client()
    
    return client

@pytest.fixture(scope='module')
def processed_data(client):
    processed_data = client.process_rundata(
        rundata=mock.mockdata)

    return processed_data

def test_can_create_rundata_client(client):
    assert isinstance(client, rdc.Client)

def test_client_has_handler_attribute(client):
    assert hasattr(client, 'handler')

def test_handler_attr_is_chain_of_handlers(client):
    assert isinstance(client.handler, hdlr.HandlerBase)

def test_client_has_process_rundata_method(client):
    assert 'process_rundata' in dir(client)

def test_client_process_rundata_method_is_callable(client):
    assert callable(client.process_rundata)

def test_client_process_rundata_method_takes_rundata_kwarg(client):
    with pytest.raises(TypeError):
        client.process_rundata()

def test_process_rundata_returns_list(client):
    assert client.process_rundata(rundata={}) == []

def test_process_rundata_returns_list_of_dicts(processed_data):
    assert len(processed_data)
    assert all([isinstance(run, dict) for run in processed_data])

def test_expected_12_mock_runs_return_9_valid_runs(processed_data):
    assert len(processed_data) == 9

def test_walk_returns_empty_list(client):
    rundata = {'WALK': mock.mockdata['WALK']} 
    processed_data = client.process_rundata(rundata=rundata)
    assert not len(processed_data)

def test_missing_data_returns_empty_list(client):
    rundata = {'MISSING_VITAL_DATA': mock.mockdata['MISSING_VITAL_DATA']} 
    processed_data = client.process_rundata(rundata=rundata)
    assert not len(processed_data)

def test_treadmill_run_returns_exact_distance(client):
    rundata = {'TREADMILL_RUN': mock.mockdata['TREADMILL_RUN']}
    raw_distance =  mock.mockdata['TREADMILL_RUN'][0]['distance']
    processed_data = client.process_rundata(rundata=rundata)
    assert processed_data[0]['distance'] == raw_distance

def test_treadmill_run_returns_empty_list(client):
    rundata = {'SHORT_RUN': mock.mockdata['SHORT_RUN']}
    processed_data = client.process_rundata(rundata=rundata)
    assert not len(processed_data)

def test_post_garmin_run_returns_exact_distance(client):
    rundata = {'POST_GARMIN_RUN': mock.mockdata['POST_GARMIN_RUN']}
    raw_distance =  mock.mockdata['POST_GARMIN_RUN'][0]['distance']
    processed_data = client.process_rundata(rundata=rundata)
    assert processed_data[0]['distance'] == raw_distance

def test_valid_run_returns_short_run_distance(client):
    rundata = {'VALID_RUN': mock.mockdata['VALID_RUN']}
    raw_distance =  mock.mockdata['VALID_RUN'][0]['distance']
    processed_data = client.process_rundata(rundata=rundata)
    assert processed_data[0]['distance'] == settings.SHORT_RUN_DISTANCE

def test_long_run_returns_long_run_distance(client):
    rundata = {'LONG_RUN': mock.mockdata['LONG_RUN']}
    raw_distance =  mock.mockdata['LONG_RUN'][0]['distance']
    processed_data = client.process_rundata(rundata=rundata)
    assert processed_data[0]['distance'] == settings.LONG_RUN_DISTANCE

def test_pre_housemove_run_returns_pre_housemove_distance(client):
    rundata = {'PRE_MOVE_RUN': mock.mockdata['PRE_MOVE_RUN']}
    raw_distance =  mock.mockdata['PRE_MOVE_RUN'][0]['distance']
    processed_data = client.process_rundata(rundata=rundata)
    assert processed_data[0]['distance'] == settings.HOUSEMOVE_DISTANCE

def test_post_lockdown_run_returns_post_lockdown_distance(client):
    rundata = {'POST_LOCKDOWN_RUN': mock.mockdata['POST_LOCKDOWN_RUN']}
    raw_distance =  mock.mockdata['POST_LOCKDOWN_RUN'][0]['distance']
    processed_data = client.process_rundata(rundata=rundata)
    assert processed_data[0]['distance'] == settings.POST_LOCKDOWN_DISTANCE
    
def test_two_runs_on_same_day_returns_two_runs(client):
    rundata = {'RUN_DATE': mock.mockdata['RUN_DATE']}
    processed_data = client.process_rundata(rundata=rundata)
    assert len(processed_data) == len(rundata['RUN_DATE'])

def test_run_data_has_adjusted_date_attr(client):
    rundata = {'VALID_RUN': mock.mockdata['VALID_RUN']}
    processed_data = client.process_rundata(rundata=rundata)
    assert 'adjusted_date' in processed_data[0].keys()
