import os
import sys
import pytest

ROOTDIR = os.path.dirname(
    os.path.dirname(
    os.path.dirname(__file__)))

sys.path = [ROOTDIR] + sys.path

from runTracker.src import rundataclient
from runTracker.src import runtracker as rt
from runTracker.src import dataconverter as dataconv


################
### FIXTURES ###
################

@pytest.fixture(scope='module')
def dconverter(rundata):
    dconverter = dataconv.DataConverter()
    return dconverter

@pytest.fixture(scope='module')
def rundata():
    client = rundataclient.Client()
    rtracker = rt.RunTracker(use_mocks=True, client=client)
    rtracker.gather_run_data()
    rtracker.process_run_data()

    return rtracker.runs

@pytest.fixture(scope='module')
def converteddata(dconverter, rundata):
    converteddata = dconverter.convert_data(rundata=rundata)
    return converteddata


################
#### TESTS #####
################

def test_data_converter_class_creation(dconverter):
    assert isinstance(dconverter, dataconv.DataConverter)

def test_data_converter_takes_input_data(dconverter):
    with pytest.raises(TypeError):
        dconverter = dataconv.DataConverter()
        dconverter.convert_data()

def test_data_converter_has_convert_data_fn(dconverter):
    assert 'convert_data' in [func for func in dir(dconverter)
        if callable(getattr(dconverter, func))]

def test_convert_data_returns_dict(dconverter, rundata):
    result = dconverter.convert_data(rundata=rundata)
    assert isinstance(result, dict)

def test_convert_data_dict_contains_three_keys(dconverter, rundata):
    result = dconverter.convert_data(rundata=rundata)
    assert len(result) == 3

def test_convert_data_has_required_keys(dconverter, rundata):
    result = dconverter.convert_data(rundata=rundata)
    keys = ['date', 'speed', 'pace']
    assert all([key in result.keys() for key in keys])

def test_run_data_dict_values_have_9_runs(converteddata, rundata):
    assert len(rundata) == 9
    assert all([len(converteddata[key]) == 9 for key in converteddata.keys()])

def test_convert_data_returns_dict_of_lists(converteddata):
    assert all([isinstance(value, list) for value in converteddata.values()])

def test_convert_data_lists_same_length_as_run_data(rundata, converteddata):
    assert all([len(value) == len(rundata) for value in converteddata.values()])
