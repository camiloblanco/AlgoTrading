import numpy as np
import pandas as pd
from scipy.stats import linregress


class White_Strategy():
    
     # Reads a CSV timeseries and strores in self.series using the time colum as index
    def __init__(self, csv_file_name):
        self.series = pd.read_csv(csv_file_name)
        #The next line crashes becuase we need and integer index... learn how to interate over time series DF
        #self.series = self.series.set_index('time')
        self.series['state'] = np.nan
        self.series['long_signal'] = np.nan
        self.series['short_signal'] = np.nan

    # Generates long or short signal depending on the state
    def wr_state_analyzer(self, state):

        if state == 3 or state == 4:
            long_signal = 1
            short_signal = 0
        elif state == 6 or state == 7:
            long_signal = 0
            short_signal = -1
        else:
            long_signal = 0
            short_signal = 0
        
        return long_signal, short_signal
    

    # State macine implementing the white robot strategy without slope
    def simple_white_strat(self):
        
        state = 1
        long_list =[0]
        short_list=[0]
        
        for index in range(1, len(self.series)):
            
            curr_SMA_14 = self.series['SMA_14'].loc[index]
            curr_SMA_21 = self.series['SMA_21'].loc[index]
            curr_SMA_40 = self.series['SMA_40'].loc[index]
            previous_SMA_14 = self.series['SMA_14'].iloc[index-1]
            previous_SMA_21 = self.series['SMA_21'].iloc[index-1]
            previous_SMA_40 = self.series['SMA_40'].iloc[index-1]
            
            if state == 1:
                if (previous_SMA_14 < previous_SMA_21) and (curr_SMA_14 > curr_SMA_21):
                    state = 2
                elif (previous_SMA_14 > previous_SMA_21) and (curr_SMA_14 < curr_SMA_21):
                    state = 5
            elif state == 2:
                if (previous_SMA_14 < previous_SMA_40) and (curr_SMA_14 > curr_SMA_40):
                    state = 3
            elif state == 3:
                if (previous_SMA_14 > previous_SMA_21) and (curr_SMA_14 < curr_SMA_21):
                    state = 4
            elif state == 4:
                if (previous_SMA_14 > previous_SMA_40) and (curr_SMA_14 < curr_SMA_40):
                    state = 1
            elif state == 5:
                if(previous_SMA_14 > previous_SMA_40) and (curr_SMA_14 < curr_SMA_40):
                    state = 6
            elif state == 6:
                if(previous_SMA_14 < previous_SMA_21) and (curr_SMA_14 > curr_SMA_21):
                    state = 7
            elif state == 7:
                if(previous_SMA_14 < previous_SMA_40) and (curr_SMA_14 > curr_SMA_40):
                    state = 1

            self.series['state'].loc[index] = state
            self.series['long_signal'].loc[index], self.series['short_signal'].loc[index] = self.wr_state_analyzer(state)
        
        return self.series


    # Saves a CSV file for  data of a certain asset class
    def save_CSV_file(self, pandas_Dataframe, csv_file_name):
        pandas_Dataframe.to_csv(csv_file_name)




if __name__=='__main__':
    fileName = "SPX500_H4_SIGNALS.CSV"
    White_Strat = White_Strategy(fileName)
    Asset_Signals = White_Strat.moving_avg_14_21_40()
    Asset_Signals.to_csv('Asset_Signals.csv')

