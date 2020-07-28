import os
import sys
import pytest

ROOTDIR = os.path.dirname(
    os.path.dirname(
    os.path.dirname(__file__)))

sys.path = [ROOTDIR] + sys.path

from runTracker.src import datadisplayer as datadis


################
### FIXTURES ###
################

@pytest.fixture(scope='module')
def ddisplayer():
    ddisplayer = datadis.DataDisplayer()
    return ddisplayer


################
#### TESTS #####
################

def test_data_displayer_class_creation(ddisplayer):
    assert isinstance(ddisplayer, datadis.DataDisplayer)

def test_data_displayer_has_display_data_fn(ddisplayer):
    assert 'display_data' in [func for func in dir(ddisplayer)
        if callable(getattr(ddisplayer, func))]