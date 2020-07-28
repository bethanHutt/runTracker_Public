import os
import sys
import pytest
import datetime

ROOTDIR = os.path.dirname(
    os.path.dirname(
    os.path.dirname(__file__)))

sys.path = [ROOTDIR] + sys.path

from runTracker.src import rundatahandler as hdlr
from runTracker.src import settings
from runTracker.mocks import mockdata as mock

assert ROOTDIR in hdlr.__file__
assert ROOTDIR in mock.__file__
assert ROOTDIR in settings.__file__



############################
#### HANDLER BASE CLASS ####
############################


@pytest.fixture(scope='module')
def handlerbase():
    baseclass = hdlr.HandlerBase(successor=None)
    
    return baseclass

def test_can_create_handler_base_class(handlerbase):
    assert isinstance(handlerbase, hdlr.HandlerBase)

def test_base_class_has_successor_attribute(handlerbase):
    assert hasattr(handlerbase, '_successor')

def test_base_class_has_handle_method(handlerbase):
    assert 'handle' in [func for func in dir(handlerbase)
        if callable(getattr(handlerbase, func))]

def test_base_class_has_private_handle_method(handlerbase):
    assert '_handle' in [func for func in dir(handlerbase)
        if callable(getattr(handlerbase, func))]

def test_handle_method_needs_rundata_kwarg(handlerbase):
    with pytest.raises(TypeError):
        handlerbase.handle()

def test_private_handle_method_needs_rundata_kwarg(handlerbase):
    with pytest.raises(TypeError):
        handlerbase._handle()

def test_base_class_private_handle_raises_error(handlerbase):
    with pytest.raises(NotImplementedError):
        handlerbase._handle(rundata=None)

def test_base_class_must_have_successor():
    with pytest.raises(TypeError):
        baseclass = hdlr.HandlerBase()



###############################
#### DATA VALIDITY HANDLER ####
###############################


@pytest.fixture(scope='module')
def datavalidator():
    valididator = hdlr.DataValidHandler(successor=None)
    
    return valididator


def test_can_create_valid_data_handler(datavalidator):
    assert isinstance(datavalidator, hdlr.DataValidHandler)

def test_datavalidhandler_is_child_of_base_class(datavalidator):
    assert issubclass(hdlr.DataValidHandler, hdlr.HandlerBase)

def test_that_providing_wrong_data_type_returns_none(datavalidator):
    assert datavalidator._handle(rundata="") is None

def test_that_providing_empty_data_type_returns_none(datavalidator):
    assert datavalidator._handle(rundata={}) is None

def test_that_providing_valid_data_returns_true(datavalidator):
    data = mock.mockdata['VALID_RUN'][0]
    assert datavalidator._handle(
        rundata=data)

def test_that_invalid_data_with_missing_attrs_returns_none(datavalidator):
    data = mock.mockdata['MISSING_VITAL_DATA'][0]
    assert datavalidator._handle(rundata=data) is None



##########################
#### RUN TYPE HANDLER ####
##########################


@pytest.fixture(scope='module')
def runtypehandler():
    runtypehandler = hdlr.RunTypeHandler(successor=None)
    
    return runtypehandler



def test_can_create_runtype_handler(runtypehandler):
    assert isinstance(runtypehandler, hdlr.RunTypeHandler)
    
def test_giving_walk_to_runtypehandler_returns_none(runtypehandler):
    data = mock.mockdata['WALK'][0]
    assert runtypehandler._handle(rundata=data) is None

def test_giving_valid_run_to_runtypehandler_returns_true(runtypehandler):
    data = mock.mockdata['VALID_RUN'][0]
    assert runtypehandler._handle(rundata=data)

def test_giving_walk_to_data_valid_handler_passes_to_runtype_returns_none():
    data = mock.mockdata['WALK'][0]
    handler = hdlr.DataValidHandler(
        successor=hdlr.RunTypeHandler(
            successor=None))
    assert handler.handle(rundata=data) is None

def test_giving_treadmil_to_data_valid_handler_passes_to_runtype_returns_true():
    data = mock.mockdata['TREADMILL_RUN'][0]
    handler = hdlr.DataValidHandler(
        successor=hdlr.RunTypeHandler(
            successor=hdlr.DefaultHandler(None)))
    assert handler.handle(rundata=data) == data


################################
######## DATE HANDLER ##########
################################

@pytest.fixture(scope='module')
def dateconverter():
    dateconverter = hdlr.DateConverter(successor=None)
    
    return dateconverter

def test_can_create_date_converter(dateconverter):
    assert isinstance(dateconverter, hdlr.DateConverter)

def test_dateconverter_with_valid_run_returns_true(dateconverter):
    data = mock.mockdata['VALID_RUN'][0]

    assert dateconverter.handle(rundata=data) is True

def test_dateconverter_adds_adjusted_date_key(dateconverter):
    data = mock.mockdata['VALID_RUN'][0]

    stack = hdlr.DataValidHandler(
        hdlr.RunTypeHandler(
            hdlr.DateConverter(
                hdlr.TreadmillHandler(
                    hdlr.GarminDateHandler(
                        hdlr.ShortDistanceHandler(
                            hdlr.HouseMoveHandler(
                                hdlr.LockdownHandler(
                                    hdlr.LongRunHandler(
                                        hdlr.DefaultHandler(None))))))))))

    processed_data = stack.handle(rundata=data)
    assert 'adjusted_date' in processed_data.keys()
    assert processed_data['adjusted_date'] == datetime.datetime(2020, 2, 18, 0, 0)


################################
#### TREADMILL TYPE HANDLER ####
################################


@pytest.fixture(scope='module')
def treadmillhandler():
    treadmillhandler = hdlr.TreadmillHandler(successor=None)
    
    return treadmillhandler


def test_can_create_treadmill_handler(treadmillhandler):
    assert isinstance(treadmillhandler, hdlr.TreadmillHandler)

def test_input_treadmill_run_returns_rundata(treadmillhandler):
    data = mock.mockdata['TREADMILL_RUN'][0]

    assert treadmillhandler.handle(rundata=data) == data

def test_input_non_treadmill_data_returns_true(treadmillhandler):
    data = mock.mockdata['VALID_RUN'][0]

    assert treadmillhandler.handle(rundata=data) is True


################################
#### GARMIN DATE HANDLER #######
################################

@pytest.fixture(scope='module')
def garminhandler():
    garminhandler = hdlr.GarminDateHandler(successor=None)
    
    return garminhandler

def test_can_create_garmindatehandler(garminhandler):
    assert isinstance(garminhandler, hdlr.GarminDateHandler)

def test_garmindatehandler_needs_successor():
    with pytest.raises(TypeError):
        garminhandler = hdlr.GarminDateHandler()

def test_post_garmin_input_returns_rundata(garminhandler):
    data = mock.mockdata['POST_GARMIN_RUN'][0]
    runmonth, runday, runyear = data['date'].split('/')
    run_date = datetime.datetime(int(runyear), int(runmonth), int(runday))
    data['adjusted_date'] = run_date

    assert garminhandler.handle(rundata=data) == data

def test_pre_garming_input_returns_true(garminhandler):
    data = mock.mockdata['VALID_RUN'][0]

    assert garminhandler.handle(rundata=data)

def test_post_garmin_runs_through_chain_of_command():
    data = mock.mockdata['POST_GARMIN_RUN'][0]

    stack = hdlr.DataValidHandler(
        hdlr.RunTypeHandler(
            hdlr.DateConverter(
                hdlr.TreadmillHandler(
                    hdlr.GarminDateHandler(
                        hdlr.DefaultHandler(None))))))

    assert stack.handle(rundata=data) == data


################################
#### SHORT DISTANCE HANDLER ####
################################

@pytest.fixture(scope='module')
def shortdistancehandler():
    shortdistancehandler = hdlr.ShortDistanceHandler(successor=None)
    
    return shortdistancehandler


def test_can_create_shortdistancehandler(shortdistancehandler):
    assert isinstance(shortdistancehandler, hdlr.ShortDistanceHandler)

def test_shortdistancehandler_needs_successor():
    with pytest.raises(TypeError):
        shortdistancehandler = hdlr.ShortDistanceHandler()

def test_short_run_in_shortdistancehandler_returns_none(shortdistancehandler):
    data = mock.mockdata['SHORT_RUN'][0]

    assert shortdistancehandler.handle(rundata=data) is None

def test_long_run_in_shortdistancehandler_returns_rundata(shortdistancehandler):
    data = mock.mockdata['VALID_RUN'][0]

    assert shortdistancehandler.handle(rundata=data) is True

def test_long_run_in_stack_returns_rundata():
    data = mock.mockdata['VALID_RUN'][0]
    stack = hdlr.DataValidHandler(
        hdlr.RunTypeHandler(
            hdlr.TreadmillHandler(
                hdlr.GarminDateHandler(
                    hdlr.ShortDistanceHandler(
                        hdlr.DefaultHandler(None))))))

    assert stack.handle(rundata=data) 



################################
#### PRE HOUSEMOVE HANDLER #####
################################

@pytest.fixture(scope='module')
def housemovehandler():
    housemovehandler = hdlr.HouseMoveHandler(successor=None)
    
    return housemovehandler

def test_can_create_housemovehandler(housemovehandler):
    assert isinstance(housemovehandler, hdlr.HouseMoveHandler)

def test_housemovehandler_needs_successor():
    with pytest.raises(TypeError):
        housemovehandler = hdlr.HouseMoveHandler()

def test_pre_move_run_returns_rundata(housemovehandler):
    data = mock.mockdata['PRE_MOVE_RUN'][0]
    runmonth, runday, runyear = data['date'].split('/')
    run_date = datetime.datetime(int(runyear), int(runmonth), int(runday))
    data['adjusted_date'] = run_date

    assert isinstance(housemovehandler.handle(rundata=data), dict)

def test_pre_move_run_returns_adjusted_distance(housemovehandler):
    data = mock.mockdata['PRE_MOVE_RUN'][0]
    assert housemovehandler.handle(
        rundata=data)['distance'] == settings.HOUSEMOVE_DISTANCE

def test_pre_move_run_stores_original_distance(housemovehandler):
    data = mock.mockdata['PRE_MOVE_RUN'][0]
    assert 'original_distance' in housemovehandler.handle(rundata=data).keys()

def test_pre_move_run_stores_correct_original_distance(housemovehandler):
    data = mock.mockdata['PRE_MOVE_RUN'][0]
    assert housemovehandler.handle(
        rundata=data)['original_distance'] == data['distance']

def test_post_move_run_returns_true(housemovehandler):
    data = mock.mockdata['VALID_RUN'][0]
    assert housemovehandler.handle(rundata=data) is True

def test_pre_move_run_in_stack_returns_adjusted_distance():
    data = mock.mockdata['PRE_MOVE_RUN'][0]
    runmonth, runday, runyear = data['date'].split('/')
    run_date = datetime.datetime(int(runyear), int(runmonth), int(runday))
    data['adjusted_date'] = run_date
    
    stack = hdlr.DataValidHandler(
        hdlr.RunTypeHandler(
            hdlr.DateConverter(
                hdlr.TreadmillHandler(
                    hdlr.GarminDateHandler(
                        hdlr.ShortDistanceHandler(
                            hdlr.HouseMoveHandler(
                                hdlr.DefaultHandler(None))))))))

    assert stack.handle(
        rundata=data)['distance'] == settings.HOUSEMOVE_DISTANCE
    assert 'original_distance' in stack.handle(rundata=data).keys()
    assert stack.handle(
        rundata=data)['original_distance'] == data['distance']


################################
####### PRE 5K HANDLER #########
################################

@pytest.fixture(scope='module')
def fivekmhandler():
    fivekmhandler = hdlr.FiveKMDateHandler(successor=None)
    return fivekmhandler

def test_can_create_fivekmhandler(fivekmhandler):
    assert isinstance(fivekmhandler, hdlr.FiveKMDateHandler)

def test_fivekmhandler_needs_successor():
    with pytest.raises(TypeError):
        fivekmhandler = hdlr.FiveKMDateHandler()

def test_pre_five_km_run_returns_rundata(fivekmhandler):
    data = mock.mockdata['PRE_FIVEKM_RUN'][0]
    runmonth, runday, runyear = data['date'].split('/')
    run_date = datetime.datetime(int(runyear), int(runmonth), int(runday))
    data['adjusted_date'] = run_date

    assert isinstance(fivekmhandler.handle(rundata=data), dict)

def test_post_five_km_run_returns_true(fivekmhandler):
    data = mock.mockdata['VALID_RUN'][0]
    runmonth, runday, runyear = data['date'].split('/')
    run_date = datetime.datetime(int(runyear), int(runmonth), int(runday))
    data['adjusted_date'] = run_date

    assert fivekmhandler.handle(rundata=data) is True

def test_pre_five_km_run_in_stack_returns_rundata():
    data = mock.mockdata['PRE_FIVEKM_RUN'][0]
    runmonth, runday, runyear = data['date'].split('/')
    run_date = datetime.datetime(int(runyear), int(runmonth), int(runday))
    data['adjusted_date'] = run_date

    stack = hdlr.DataValidHandler(
        hdlr.RunTypeHandler(
            hdlr.DateConverter(
                hdlr.TreadmillHandler(
                    hdlr.GarminDateHandler(
                        hdlr.ShortDistanceHandler(
                            hdlr.HouseMoveHandler(
                                hdlr.FiveKMDateHandler(
                                    hdlr.DefaultHandler(None)))))))))

    assert stack.handle(rundata=data)['distance'] == data['distance']

################################
#### POST LOCKDOWN HANDLER #####
################################

@pytest.fixture(scope='module')
def lockdownhandler():
    lockdownhandler = hdlr.LockdownHandler(successor=None)
    
    return lockdownhandler

def test_can_create_lockdownhandler(lockdownhandler):
    assert isinstance(lockdownhandler, hdlr.LockdownHandler)

def test_lockdownhandler_needs_successor():
    with pytest.raises(TypeError):
        lockdownhandler = hdlr.LockdownHandler()

def test_post_lockdown_run_returns_rundata(lockdownhandler):
    data = mock.mockdata['POST_LOCKDOWN_RUN'][0]
    runmonth, runday, runyear = data['date'].split('/')
    run_date = datetime.datetime(int(runyear), int(runmonth), int(runday))
    data['adjusted_date'] = run_date

    assert isinstance(lockdownhandler.handle(rundata=data), dict)

def test_post_lockdown_run_returns_adjusted_distance(lockdownhandler):
    data = mock.mockdata['POST_LOCKDOWN_RUN'][0]
    assert lockdownhandler.handle(
        rundata=data)['distance'] == settings.POST_LOCKDOWN_DISTANCE

def test_post_lockdown_run_stores_original_distance(lockdownhandler):
    data = mock.mockdata['POST_LOCKDOWN_RUN'][0]
    assert 'original_distance' in lockdownhandler.handle(rundata=data).keys()

def test_post_lockdown_run_stores_correct_original_distance(lockdownhandler):
    data = mock.mockdata['POST_LOCKDOWN_RUN'][0]
    runmonth, runday, runyear = data['date'].split('/')
    run_date = datetime.datetime(int(runyear), int(runmonth), int(runday))
    data['adjusted_date'] = run_date
    assert lockdownhandler.handle(
        rundata=data)['original_distance'] == data['distance']

def test_pre_lockdown_run_returns_true(lockdownhandler):
    data = mock.mockdata['VALID_RUN'][0]
    assert lockdownhandler.handle(rundata=data) is True

def test_post_lockdown_run_in_stack_returns_adjusted_distance():
    data = mock.mockdata['POST_LOCKDOWN_RUN'][0]

    stack = hdlr.DataValidHandler(
        hdlr.RunTypeHandler(
            hdlr.DateConverter(
                hdlr.TreadmillHandler(
                    hdlr.GarminDateHandler(
                        hdlr.ShortDistanceHandler(
                            hdlr.HouseMoveHandler(
                                hdlr.LockdownHandler(
                                    hdlr.DefaultHandler(None)))))))))

    assert stack.handle(
        rundata=data)['distance'] == settings.POST_LOCKDOWN_DISTANCE
    assert 'original_distance' in stack.handle(rundata=data).keys()
    assert stack.handle(
        rundata=data)['original_distance'] == data['distance']


################################
#### LONG RUN HANDLER ##########
################################

@pytest.fixture(scope='module')
def longrunhandler():
    longrunhandler = hdlr.LongRunHandler(successor=None)
    
    return longrunhandler

def test_can_create_longrunhandler(longrunhandler):
    assert isinstance(longrunhandler, hdlr.LongRunHandler)

def test_longrunhandler_needs_successor():
    with pytest.raises(TypeError):
        longrunhandler = hdlr.LongRunHandler()

def test_long_run_returns_rundata(longrunhandler):
    data = mock.mockdata['LONG_RUN'][0]
    assert isinstance(longrunhandler.handle(rundata=data), dict)

def test_long_run_returns_adjusted_distance(longrunhandler):
    data = mock.mockdata['LONG_RUN'][0]
    assert longrunhandler.handle(
        rundata=data)['distance'] == settings.LONG_RUN_DISTANCE

def test_long_run_stores_original_distance(longrunhandler):
    data = mock.mockdata['LONG_RUN'][0]
    assert 'original_distance' in longrunhandler.handle(rundata=data).keys()

def test_long_run_stores_correct_original_distance(longrunhandler):
    data = mock.mockdata['LONG_RUN'][0]
    assert longrunhandler.handle(
        rundata=data)['original_distance'] == data['distance']

def test_short_run_returns_true(longrunhandler):
    data = mock.mockdata['VALID_RUN'][0]
    assert longrunhandler.handle(rundata=data) is True

def test_short_run_in_stack_returns_adjusted_distance():
    data = mock.mockdata['LONG_RUN'][0]
    stack = hdlr.DataValidHandler(
        hdlr.RunTypeHandler(
            hdlr.DateConverter(
                hdlr.TreadmillHandler(
                    hdlr.GarminDateHandler(
                        hdlr.ShortDistanceHandler(
                            hdlr.HouseMoveHandler(
                                hdlr.LockdownHandler(
                                    hdlr.LongRunHandler(
                                        hdlr.DefaultHandler(None))))))))))

    assert stack.handle(
        rundata=data)['distance'] == settings.LONG_RUN_DISTANCE
    assert 'original_distance' in stack.handle(rundata=data).keys()
    assert stack.handle(
        rundata=data)['original_distance'] == data['distance']


################################
#### DEFAULT RUN HANDLER #######
################################

@pytest.fixture(scope='module')
def defaulthandler():
    defaulthandler = hdlr.DefaultHandler(successor=None)
    
    return defaulthandler

def test_can_create_default_run_handler(defaulthandler):
    assert isinstance(defaulthandler, hdlr.DefaultHandler)

def test_defaulthandler_needs_successor():
    with pytest.raises(TypeError):
        longrunhandler = hdlr.LongRunHandler()

def test_valid_run_returns_rundata(defaulthandler):
    data = mock.mockdata['VALID_RUN'][0]
    assert isinstance(defaulthandler.handle(rundata=data), dict)

def test_valid_run_returns_adjusted_distance(defaulthandler):
    data = mock.mockdata['VALID_RUN'][0]
    assert defaulthandler.handle(
        rundata=data)['distance'] == settings.SHORT_RUN_DISTANCE

def test_valid_run_stores_original_distance(defaulthandler):
    data = mock.mockdata['VALID_RUN'][0]
    assert 'original_distance' in defaulthandler.handle(rundata=data).keys()

def test_valid_run_stores_correct_original_distance(defaulthandler):
    data = mock.mockdata['VALID_RUN'][0]
    assert defaulthandler.handle(
        rundata=data)['original_distance'] == data['distance']

def test_pvalid_run_in_stack_returns_adjusted_distance():
    data = mock.mockdata['VALID_RUN'][0]
    stack = hdlr.DataValidHandler(
        hdlr.RunTypeHandler(
            hdlr.TreadmillHandler(
                hdlr.GarminDateHandler(
                    hdlr.ShortDistanceHandler(
                        hdlr.HouseMoveHandler(
                            hdlr.LockdownHandler(
                                hdlr.LongRunHandler(
                                    hdlr.DefaultHandler(None)))))))))

    assert stack.handle(
        rundata=data)['distance'] == settings.SHORT_RUN_DISTANCE
    assert 'original_distance' in stack.handle(rundata=data).keys()
    assert stack.handle(
        rundata=data)['original_distance'] == data['distance']