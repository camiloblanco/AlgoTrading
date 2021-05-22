import requests
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date
import tables as tb
import plotly.graph_objects as go


class Signal_Gen():

    def __init__(self):
        self.Merged_candle_data = tb.open_file('Merge_candle_Dataframe.h5','r')
        table = self.Merged_candle_data.root.quote.z4
        c = pd.DataFrame.from_records(table.read())
        print(c)

    def Simple_moving_average(self, rolling_window):
        #print(self.Merged_candle_data.root.data[:3])
        #self.Merged_candle_data.close()
        pass





if __name__ == '__main__':
    s_g = Signal_Gen()
    s_g.Simple_moving_average(2)

