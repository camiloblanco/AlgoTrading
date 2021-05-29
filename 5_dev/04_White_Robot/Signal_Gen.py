import requests
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import date
import tables as tb
from tables import *
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px


class Signal_Gen():

    #Constructors
    
    # Reads a CSV timeseries and strores in self.series
    def __init__(self, csv_file_name):
        self.series = pd.read_csv(csv_file_name)
        

    def Simple_moving_average(self, rolling_window, window_name):
        self.series[window_name] = self.series['mid_c'].rolling(window=rolling_window).mean()
        return self.series



