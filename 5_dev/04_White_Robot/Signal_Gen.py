import requests
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import date
import tables as tb
from tables import *
import plotly.graph_objects as go
import matplotlib as plt


class Signal_Gen():

    def __init__(self,Candle_h5_file):
        self.Candle_h5_file = Candle_h5_file
        self.table = self.Candle_h5_file.root.candledata.candletable
        time = [x['time'] for x in self.table.iterrows()]
        time = [x.decode('utf-8') for x in time]
        self.Time_Points = [datetime.strptime(x, '%Y-%m-%d %H:%M:%S') for x in time]
        self.mid_close_points = [x['mid_c'] for x in self.table.iterrows()]
        self.mid_close_points = pd.DataFrame(self.mid_close_points)
        self.Candle_h5_file.close()


    def Simple_moving_average(self, rolling_window):
        SMA_Data = self.mid_close_points.rolling(window=rolling_window).mean()
        return SMA_Data

        
    #def Simple_moving_average(self, rolling_window_1,rolling_window_2, rolling_window_3):
     #   SMA_Data_14 = self.mid_close_points.rolling(window=rolling_window_1).mean()
      #  SMA_Data_21 = self.mid_close_points.rolling(window=rolling_window_2).mean()
       # SMA_Data_50 = self.mid_close_points.rolling(window=rolling_window_3).mean()
        

if __name__ == '__main__':
    Candle_h5_file = open_file('Candle_h5_file.h5', "a")
    s_g = Signal_Gen(Candle_h5_file)
    fig = s_g.Simple_moving_average(14,21,50)
    fig.update_layout(
        title="Moving_Averages",
        xaxis_title="Time",
        yaxis_title="close_price",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        ))
    fig.show()



