import os
import sys
import numpy
import pandas
import matplotlib.pyplot as plt

ROOTDIR = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__)))
sys.path = [ROOTDIR] + sys.path

from runTracker.src import settings


class DataDisplayer():
    def display_data(self, rundata, datatype):
        data_frame = pandas.DataFrame(rundata, columns=['date', datatype])

        data_frame.loc[:, 'date'] = pandas.to_datetime(
            data_frame.loc[:, 'date'], format="%d-%b-%y")

        y_values = data_frame.loc[:, datatype]
        x_values = numpy.linspace(0, 1, len(data_frame.loc[:, datatype]))
        poly_degree = 3

        coefficients = numpy.polyfit(x_values, y_values, poly_degree)
        poly_equation = numpy.poly1d(coefficients)
        line_of_best_fit = poly_equation(x_values)

        plt.figure(figsize=settings.GRAPH_SIZE)
        plt.plot(data_frame.loc[:, 'date'], data_frame.loc[:, datatype],
            settings.GRAPH_FORMAT)
        plt.plot(data_frame.loc[:, 'date'], line_of_best_fit)

        start_date = data_frame.head(1)['date'].array[0].date()
        end_date = data_frame.tail(1)['date'].array[0].date()

        plt.title(f'Run Tracker - {start_date} to {end_date}')

        plt.ylabel(datatype.capitalize() + '(km)')
        plt.xlabel('Date')
        
        plt.savefig('Run_Data.png')
        plt.show()
