import requests
import numpy as np
import pandas as pd
from scipy.stats import linregress
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
        
    # Moving average method
    def Simple_moving_average(self, rolling_window, window_name):
        self.series[window_name] = self.series['mid_c'].rolling(window=rolling_window).mean()
        return self.series
    
    # Method to get the slope of an Array and index
    # From https://stackoverflow.com/questions/58499114/calculate-a-rolling-regression-in-pandas-and-store-the-slope
    def get_slope(self,array):
        y = np.array(array)
        x = np.arange(len(y))
        slope, intercept, r_value, p_value, std_err = linregress(x,y)
        return slope


    # Moving Slope method
    def moving_slope(self, rolling_window, window_name):
        
        self.series[window_name] = self.series['mid_c'].rolling(window=rolling_window).mean()
        
        self.series[window_name] = self.series['mid_c'].rolling(window=rolling_window).apply(self.get_slope, raw=False)

        
        return self.series



