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

    def __init__(self, Merged_Candle_File):
        self.Merged_Candle_Data = Merged_Candle_File
        self.Time_Point = self.Merged_Candle_Data['time']



    def Simple_moving_average(self, rolling_window, window_name):

        self.Merged_Candle_Data[window_name] = self.Merged_Candle_Data['mid_c'].rolling(window=rolling_window).mean()
        self.Merged_Candle_Data.to_csv("Merged_candle_data.csv")
        return self.Merged_Candle_Data['SMA_14']

        
    #def Simple_moving_average(self, rolling_window_1,rolling_window_2, rolling_window_3):
     #   SMA_Data_14 = self.mid_close_points.rolling(window=rolling_window_1).mean()
      #  SMA_Data_21 = self.mid_close_points.rolling(window=rolling_window_2).mean()
       # SMA_Data_50 = self.mid_close_points.rolling(window=rolling_window_3).mean()
        

if __name__ == '__main__':
    Merged_Candle_Dataframe = pd.read_csv("Merged_candle_data.csv")
    s_g = Signal_Gen(Merged_Candle_Dataframe)
    SMA_Data = s_g.Simple_moving_average(14,'SMA_14')
    print(SMA_Data)


