import numpy as np
import pandas as pd
from scipy.stats import linregress


class White_Strategy():

    def __init__(self, csv_filename):
        self.Asset_signals = pd.read_csv(csv_filename)


    def moving_avg_strategy(self):
        self.Asset_signals['SMA_14 > SMA_21'] = np.where((self.Asset_signals['SMA_14'] > self.Asset_signals['SMA_21']) &
                                                         (self.Asset_signals['SMA_14'].shift() < self.Asset_signals['SMA_21'].shift()), 1, 0)
        self.Asset_signals['SMA>14 > SMA_40'] = np.where((self.Asset_signals['SMA_14'] > self.Asset_signals['SMA_40']) &
                                                         (self.Asset_signals['SMA_14'].shift() < self.Asset_signals['SMA_40'].shift()), 1, 0)
        self.Asset_signals['SMA_14 < SMA_21'] = np.where((self.Asset_signals['SMA_14'] < self.Asset_signals['SMA_21']) &
                                                         (self.Asset_signals['SMA_14'].shift() > self.Asset_signals['SMA_21'].shift()), 1, 0)
        self.Asset_signals['SMA_14 < SMA_40'] = np.where((self.Asset_signals['SMA_14'] < self.Asset_signals['SMA_40']) &
                                                         (self.Asset_signals['SMA_14'].shift() > self.Asset_signals['SMA_40'].shift()), 1, 0)

        return self.Asset_signals





    