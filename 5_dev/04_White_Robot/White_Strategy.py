import numpy as np
import pandas as pd
from scipy.stats import linregress




class White_Strategy():

    def __init__(self, csv_filename):
        self.Asset_signals = pd.read_csv(csv_filename)
        self.Asset_signals['State'] = np.nan
        self.Asset_signals['Long_Signal'] = np.nan
        self.Asset_signals['Short_Signal'] = np.nan

    def simple_state_analyzer(self, state):

        if state == 1.5 or state == 1 or state == -1.5:
            long_signal = 0
            short_signal = 0
        if state == 2.0 or state == 2.5:
            long_signal = 1
            short_signal = 0
        if state == -2.0 or state == -2.5:
            long_signal = 0
            short_signal = -1
        return long_signal, short_signal

    # Creates the Long State of the SNP 500 index
    def moving_avg_14_21_40(self):
        state = 1
        for index in range(1, len(self.Asset_signals)):
            curr_SMA_14 = self.Asset_signals['SMA_14'].loc[index]
            curr_SMA_21 = self.Asset_signals['SMA_21'].loc[index]
            curr_SMA_40 = self.Asset_signals['SMA_40'].loc[index]
            previous_SMA_14 = self.Asset_signals['SMA_14'].iloc[index-1]
            previous_SMA_21 = self.Asset_signals['SMA_21'].iloc[index-1]
            previous_SMA_40 = self.Asset_signals['SMA_40'].iloc[index-1]
            if state == 1:
                if (previous_SMA_14 < previous_SMA_21) and (curr_SMA_14 > curr_SMA_21):
                    state = 1.5
                    long, short = self.simple_state_analyzer(state)
                    self.Asset_signals['Long_Signal'].loc[index] = long
                    self.Asset_signals['Short_Signal'].loc[index] = short
                elif (previous_SMA_14 > previous_SMA_21) and (curr_SMA_14 < curr_SMA_21):
                    state = -1.5
                    long, short = self.simple_state_analyzer(state)
                    self.Asset_signals['Long_Signal'].loc[index] = long
                    self.Asset_signals['Short_Signal'].loc[index] = short
                else:
                    continue
            elif state == 1.5:
                if (previous_SMA_14 < previous_SMA_40) and (curr_SMA_14 > curr_SMA_40):
                    state = 2.0
                    long, short = self.simple_state_analyzer(state)
                    self.Asset_signals['Long_Signal'].loc[index] = long
                    self.Asset_signals['Short_Signal'].loc[index] = short
                else:
                    continue
            elif state == 2.0:
                if (previous_SMA_14 > previous_SMA_21) and (curr_SMA_14 < curr_SMA_21):
                    state = 2.5
                    long, short = self.simple_state_analyzer(state)
                    self.Asset_signals['Long_Signal'].loc[index] = long
                    self.Asset_signals['Short_Signal'].loc[index] = short
                else:
                    continue
            elif state == 2.5:
                if (previous_SMA_14 > previous_SMA_40) and (curr_SMA_14 < curr_SMA_40):
                    state = 1
                    long, short = self.simple_state_analyzer(state)
                    self.Asset_signals['Long_Signal'].loc[index] = long
                    self.Asset_signals['Short_Signal'].loc[index] = short
                else:
                    continue
            elif state == -1.5:
                if(previous_SMA_14 > previous_SMA_40) and (curr_SMA_14 < curr_SMA_40):
                    state = -2.0
                    long, short = self.simple_state_analyzer(state)
                    self.Asset_signals['Long_Signal'].loc[index] = long
                    self.Asset_signals['Short_Signal'].loc[index] = short
                else:
                    continue
            elif state == -2.0:
                if(previous_SMA_14 < previous_SMA_21) and (curr_SMA_14 > curr_SMA_21):
                    state = -2.5
                    long, short = self.simple_state_analyzer(state)
                    self.Asset_signals['Long_Signal'].loc[index] = long
                    self.Asset_signals['Short_Signal'].loc[index] = short
                else:
                    continue
            elif state == -2.5:
                if(previous_SMA_14 < previous_SMA_40) and (curr_SMA_14 > curr_SMA_40):
                    state = 1
                    long, short = self.simple_state_analyzer(state)
                    self.Asset_signals['Long_Signal'].loc[index] = long
                    self.Asset_signals['Short_Signal'].loc[index] = short
                else:
                    continue
        return self.Asset_signals[['time', 'mid_c', 'Long_Signal', 'Short_Signal']]






if __name__=='__main__':
    fileName = "SPX500_H4_SIGNALS.CSV"
    White_Strat = White_Strategy(fileName)
    Asset_Signals = White_Strat.moving_avg_14_21_40()
    Asset_Signals.to_csv('Asset_Signals.csv')

