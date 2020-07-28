import os
import sys

ROOTDIR = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__)))

sys.path = [ROOTDIR] + sys.path

from runTracker.src import rundatahandler as hdlr
assert ROOTDIR in hdlr.__file__


class Client():
    def __init__(self):
        self.handler = hdlr.DataValidHandler(
            hdlr.RunTypeHandler(
                hdlr.DateConverter(
                    hdlr.TreadmillHandler(
                        hdlr.GarminDateHandler(
                            hdlr.ShortDistanceHandler(
                                hdlr.HouseMoveHandler(
                                    hdlr.FiveKMDateHandler(
                                        hdlr.LockdownHandler(
                                            hdlr.LongRunHandler(
                                                hdlr.DefaultHandler(
                                                    None)))))))))))

    def process_rundata(self, rundata):
        processed_data = []

        for daily_activities in rundata:
            for activity in rundata[daily_activities]:
                processed_run = self.handler.handle(rundata=activity)

                if not processed_run:
                    continue

                processed_data.append(processed_run)

        return processed_data
