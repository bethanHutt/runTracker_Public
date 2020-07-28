import os
import sys
import datetime

ROOTDIR = os.path.dirname(
    os.path.dirname(__file__))

sys.path = [ROOTDIR] + sys.path

from src import settings
assert ROOTDIR in settings.__file__


class HandlerBase:
    def __init__(self, successor):
        self._successor = successor

    def handle(self, rundata):
        passed = self._handle(rundata=rundata)

        if isinstance(passed, dict):
            return rundata

        if passed and self._successor:
            successor_passed = self._successor.handle(rundata=rundata)
            return successor_passed

        return passed

    def _handle(self, rundata):
        raise NotImplementedError('Must provide _handle method in subclass.')


class DataValidHandler(HandlerBase):
    def _handle(self, rundata):
        if not isinstance(rundata, dict) or not rundata:
            return

        if not all([(attr in rundata) for attr
            in settings.REQUIRED_DATA_PARAMS]):
            return

        return True


class RunTypeHandler(HandlerBase):
    def _handle(self, rundata):
        if rundata['activity_short_name'] not in settings.VALID_ACTIVITY_TYPES:
            return

        return True


class DateConverter(HandlerBase):
    def _handle(self, rundata):
        runmonth, runday, runyear = rundata['date'].split('/')
        run_date = datetime.datetime(int(runyear), int(runmonth), int(runday))

        rundata['adjusted_date'] = run_date
        return True


class TreadmillHandler(HandlerBase):
    def _handle(self, rundata):
        if rundata['activity_short_name'] == 'indoorrun':
            rundata['original_distance'] = rundata['distance']
            return rundata

        return True


class GarminDateHandler(HandlerBase):
    def _handle(self, rundata):
        (year, month, day) = settings.GARMIN_DATE
        garmin_date = datetime.datetime(year, month, day)

        if rundata['adjusted_date'] >= garmin_date:
            rundata['original_distance'] = rundata['distance']
            return rundata

        return True


class ShortDistanceHandler(HandlerBase):
    def _handle(self, rundata):
        run_distance = float(rundata['distance'])
        if run_distance < settings.MINIMUM_RUN_DISTANCE:
            return

        rundata['original_distance'] = rundata['distance']
        return True


class HouseMoveHandler(HandlerBase):
    def _handle(self, rundata):
        (year, month, day) = settings.HOUSEMOVE_DATE
        house_move_date = datetime.datetime(year, month, day)

        if rundata['adjusted_date'] < house_move_date:
            rundata['original_distance'] = rundata['distance']
            rundata['distance'] = settings.HOUSEMOVE_DISTANCE

            return rundata

        return True


class FiveKMDateHandler(HandlerBase):
    def _handle(self, rundata):
        (year, month, day) = settings.FIVE_KM_START_DATE
        five_km_start_date = datetime.datetime(year, month, day)

        if rundata['adjusted_date'] < five_km_start_date:
            if rundata['distance'] > settings.SHORT_RUN_THRESHOLD:
                return

            return rundata

        return True



class LockdownHandler(HandlerBase):
    def _handle(self, rundata):
        (year, month, day) = settings.LOCKDOWN_DATE
        lockdown_date = datetime.datetime(year, month, day)

        if rundata['adjusted_date'] >= lockdown_date:
            rundata['original_distance'] = rundata['distance']

            (year, month, day) = settings.BAD_RUN_DATE
            bad_run_date = datetime.datetime(year, month, day)

            if rundata['distance'] > settings.LONG_RUN_THRESHOLD:
                rundata['distance'] = settings.POST_LOCKDOWN_DISTANCE
            elif rundata['distance'] > settings.SHORT_RUN_THRESHOLD:
                rundata['distance'] = settings.SHORT_RUN_DISTANCE
            elif rundata['adjusted_date'] == bad_run_date:
                rundata['distance'] = settings.SHORT_RUN_DISTANCE

            return rundata

        return True


class LongRunHandler(HandlerBase):
    def _handle(self, rundata):
        run_distance = rundata['distance']
        if run_distance >= settings.LONG_RUN_THRESHOLD:
            rundata['original_distance'] = rundata['distance']
            rundata['distance'] = settings.LONG_RUN_DISTANCE

            return rundata

        return True


class DefaultHandler(HandlerBase):
    def handle(self, rundata):
        rundata['original_distance'] = rundata['distance']
        rundata['distance'] = settings.SHORT_RUN_DISTANCE

        return rundata

    def _handle(self, rundata):
        pass
