import os
import sys
import pytest

ROOTDIR = os.path.dirname(
    os.path.dirname(
    os.path.dirname(__file__)))

sys.path = [ROOTDIR] + sys.path

from runTracker.src import runobject as runobj
assert ROOTDIR in runobj.__file__


def test_run_class_creation():
    run = runobj.Run()
    assert isinstance(run, runobj.Run)

def test_fake_run_for_speed():
    rundata = {'distance' : 5.00, 'time' : 1800}
    run = runobj.Run(**rundata)
    assert run.adjusted_speed == 10

def test_fake_run_for_pace():
    rundata = {'distance' : 5.00, 'time' : 1800}
    run = runobj.Run(**rundata)
    assert run.adjusted_pace == 6