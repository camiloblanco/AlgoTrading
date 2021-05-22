import requests
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date
import tables as tb
from tables import *
import plotly.graph_objects as go
import petl as etl

class Signal_Gen():

    def __init__(self):
        self.Candle_h5_file = open_file('Candle_h5_file.h5', "a")
        table = self.Candle_h5_file.root.candledata.candletable
        self.time = [x['time'] for x in table.iterrows()]
        self.mid_c = [x['time'] for x in table.iterrows()]


    def Simple_moving_average(self, rolling_window):

        self.Candle_h5_file.close()





if __name__ == '__main__':
    s_g = Signal_Gen()
    s_g.Simple_moving_average(14)


