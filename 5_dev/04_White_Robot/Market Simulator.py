import numpy as np
import pandas as pd


class Market_Sim:
    def __init__(self, csv_filename, initial_cash, start_date, end_date):
        self.parameter = [initial_cash, start_date, end_date]
        self.series = csv_filename
        self.initial_cash = initial_cash
        self.start_date = start_date
        self.end_date = end_date
        self.series['Cash'] = np.nan
        self.series['CFD Units'] = np.nan
        self.series['CFD Intrinsic Value'] = np.nan
        self.series['Portfolio Value'] = np.nan
        self.series['Portfolio Log Returns'] = np.nan
        self.series['Last Trade Cash'] = np.nan
        self.series['Last Trade Profit'] = np.nan
        self.series['Index log returns'] = np.nan

    def simulate(self):
        end_cash = 0
        number_of_long_trades = 0
        number_of_short_trade = 0
        Total_Index_Return = 0
        Total_Strategy_Return = 0
        self.series['Cash'].loc[0] = self.parameter[0]
        self.series['CFD Units'].loc[0] = 0
        self.series['CFD Intrinsic Value'].loc[0] = self.series['mid_c'].loc[0] * self.series['CFD Units'].loc[0]
        self.series['Portfolio Value'].loc[0] = self.series['Cash'].loc[0] + self.series['CFD Intrinsic Value'].loc[0]
        self.series['Last Trade Cash'].loc[0] = self.series['Portfolio Value'].loc[0]
        self.series['Last Trade Profit'].loc[0] = (self.series['Portfolio Value'].loc[0] - self.series['Last Trade Cash'].loc[0]) / self.series['Last Trade Cash'].loc[0]
        for index in range(1, len(self.series)):
            if self.series['long_signal'].loc[index] == 1:
                self.series['Cash'].loc[index] = 0
                self.series['CFD Units'].loc[index] = self.series['Cash'].loc[index - 1] / self.series['mid_c'].loc[index]
            elif self.series['short_signal'].loc[index] == -1:
                self.series['Cash'] = self.series['CFD_Units'].loc[index-1] * self.series['mid_c'].loc[index]
                self.series['CFD_Units'].loc[index] = 0
            else:
                self.series['Cash'].loc[index] = self.series['Cash'].loc[index-1]
                self.series['CFD_Units'].loc[index] = self.series['CFD_Units'].loc[index-1]
                self.series['CFD Intrinsic Value'].loc[index] = self.series['CFD Units'].loc[index] * self.series['mid_c'].loc[index]
                self.series['Portfolio Value'].loc[index] = self.series['Cash'].loc[index] + self.series['CFD Intrinsic Value'].loc[index]
                self.series['Last Trade Cash'].loc[index] = self.series['Portfolio Value'].loc[index]
                self.series['Last Trade Profit'].loc[index] = (self.series['Portfolio Value'].loc[index] - self.series['Last Trade Cash'].loc[index]) / self.series['Last Trade Cash'].loc[index]






if __name__ == "__main__":
    order_book = pd.read_csv("WR_ORDER_BOOK.CSV")
    MS = Market_Sim(order_book, 100000, '09/04/1995', '09/05/1995')
