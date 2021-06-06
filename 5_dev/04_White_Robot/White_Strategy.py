import numpy as np
import pandas as pd
from scipy.stats import linregress


class White_Strategy():

    def __init__(self, csv_filename):
        self.Asset_signals = pd.read_csv(csv_filename)
        self.Asset_signals['State'] = np.nan
        self.Asset_signals['Long_Signal'] = np.nan
        self.Asset_signals['Short_Signal'] = np.nan

    # Creates the Long State of the SNP 500 index
    def moving_avg_14_21_40_buy(self):
        for index in range(0, len(self.Asset_signals)):
            curr_SMA_14 = self.Asset_signals['SMA_14'].loc[index]
            curr_SMA_21 = self.Asset_signals['SMA_21'].loc[index]
            curr_SMA_40 = self.Asset_signals['SMA_40'].loc[index]
            if index != 0:
                previous_SMA_14 = self.Asset_signals['SMA_14'].loc[index - 1]
                previous_SMA_21 = self.Asset_signals['SMA_21'].loc[index - 1]
                previous_SMA_40 = self.Asset_signals['SMA_40'].loc[index - 1]
                if (curr_SMA_14 > curr_SMA_21) & (previous_SMA_14 < previous_SMA_21):
                    state = 1.5
                    self.Asset_signals.at[index, 'State'] = state
                    long_signal = 0
                    self.Asset_signals.at[index, 'Long_Signal'] = long_signal
                    short_signal = 0
                    self.Asset_signals.at[index, 'Short_Signal'] = short_signal
                elif (curr_SMA_14 > curr_SMA_40) & (previous_SMA_14 < previous_SMA_40):
                    state = 2.0
                    self.Asset_signals.at[index, 'State'] = state
                    long_signal = 1
                    self.Asset_signals.at[index, 'Long_Signal'] = long_signal
                    short_signal = 0
                    self.Asset_signals.at[index, 'Short_Signal'] = short_signal
                elif (curr_SMA_14 < curr_SMA_21) & (previous_SMA_14 > previous_SMA_21):
                    state = 2.5
                    self.Asset_signals.at[index, 'State'] = state
                    long_signal = 1
                    self.Asset_signals.at[index, 'Long_Signal'] = long_signal
                    short_signal = 0
                    self.Asset_signals.at[index, 'Short_Signal'] = short_signal
                elif (curr_SMA_14 < curr_SMA_40) & (previous_SMA_14 > previous_SMA_40):
                    state = 1
                    self.Asset_signals.at[index, 'State'] = state
                    long_signal = 0
                    self.Asset_signals.at[index, 'Long_Signal'] = long_signal
                    short_signal = 0
                    self.Asset_signals.at[index, 'Short_Signal'] = short_signal
                else:
                    continue
        return self.Asset_signals['time', 'mid_c', 'State', 'Long_Signal', 'Short_Signal']

    # Creates the Short State of the SNP 500 index
    def moving_avg_14_21_40_sell(self):
        for index in range(0, len(self.Asset_signals)):
            curr_SMA_14 = self.Asset_signals['SMA_14'].loc[index]
            curr_SMA_21 = self.Asset_signals['SMA_21'].loc[index]
            curr_SMA_40 = self.Asset_signals['SMA_40'].loc[index]
            if index != 0:
                previous_SMA_14 = self.Asset_signals['SMA_14'].loc[index - 1]
                previous_SMA_21 = self.Asset_signals['SMA_21'].loc[index - 1]
                previous_SMA_40 = self.Asset_signals['SMA_40'].loc[index - 1]
                if (curr_SMA_14 < curr_SMA_21) & (previous_SMA_14 > previous_SMA_21):
                    state = -1.5
                    self.Asset_signals.at[index, 'State'] = state
                    long_signal = 0
                    self.Asset_signals.at[index, 'Long_Signal'] = long_signal
                    short_signal = 0
                    self.Asset_signals.at[index, 'Short_Signal'] = short_signal
                elif (curr_SMA_14 < curr_SMA_40) & (previous_SMA_14 > previous_SMA_40):
                    state = -2.0
                    self.Asset_signals.at[index, 'State'] = state
                    long_signal = 0
                    self.Asset_signals.at[index, 'Long_Signal'] = long_signal
                    short_signal = -1
                    self.Asset_signals.at[index, 'Short_Signal'] = short_signal
                elif (curr_SMA_14 > curr_SMA_21) & (previous_SMA_14 < previous_SMA_21):
                    state = -2.5
                    self.Asset_signals.at[index, 'State'] = state
                    long_signal = 0
                    self.Asset_signals.at[index, 'Long_Signal'] = long_signal
                    short_signal = -1
                    self.Asset_signals.at[index, 'Short_Signal'] = short_signal
                elif (curr_SMA_14 > curr_SMA_40) & (previous_SMA_14 < previous_SMA_40):
                    state = 1
                    self.Asset_signals.at[index, 'State'] = state
                    long_signal = 0
                    self.Asset_signals.at[index, 'Long_Signal'] = long_signal
                    short_signal = 0
                    self.Asset_signals.at[index, 'Short_Signal'] = short_signal
                else:
                    continue
        return self.Asset_signals['Short_Signal']

    # Concat both Frames
    def Final_Buy_Sell_Dataframe(self):
        Buy_Signal = self.moving_avg_14_21_40_buy()
        Buy_Sell_Signals = pd.DataFrame()
        Buy_Sell_Signals['Time'] = self.Asset_signals['time']
        Buy_Sell_Signals['mid_c'] = self.Asset_signals['mid_c']
        Buy_Sell_Signals['Buy'] = Buy_Signal
        return Buy_Sell_Signals
