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
        self.series['Last Trade Investment'] = np.nan
        self.series['Long_CFDs_Value'] = np.nan
        self.series['Short_CFDs_value'] = np.nan
        self.series['Current Portfolio Value'] = np.nan
        self.series['Last Trade Profit'] = np.nan
        self.series['Buy'] = np.nan
        self.series['Sell'] = np.nan

    def get_cash(self, index):
        if (self.series['CFD Units'].loc[index - 1] == 0) and (self.series['CFD Units'].loc[index] > 0):
            self.series['Cash'].loc[index] = 0
        elif (self.series['Last Trade Investment'].loc[index] == 0) and (
                self.series['Last Trade Investment'].loc[index - 1] > 0):
            self.series['Cash'].loc[index] = self.series['Current Portfolio Value'].loc[index]
        else:
            self.series['Cash'].loc[index] = self.series['Cash'].loc[index - 1]
        return self.series['Cash']

    def get_CFD_Units(self, index):
        if self.series['long_signal'].loc[index] == 0:
            self.series['CFD Units'].loc[index] = 0
        elif ((self.series['long_signal'].loc[index - 1] == 0) and (self.series['long_signal'].loc[index] == 1)) or \
                ((self.series['short_signal'].loc[index - 1] == 0) and (self.series['short_signal'].loc[index]) == -1):
            self.series['CFD Units'].loc[index] = (self.series['Cash'].loc[index - 1] / self.series['mid_c'].loc[index])
        else:
            self.series['CFD Units'].loc[index] = self.series['CFD Units'].loc[index - 1]
        return self.series['CFD Units']

    def get_Last_Trade_Investment(self, index):
        if (self.series['long_signal'].loc[index] == 0) and (self.series['short_signal'].loc[index] == 0):
            self.series['Last Trade Investment'].loc[index] = 0
        elif (self.series['CFD Units'].loc[index - 1] == 0) and (self.series['CFD Units'].loc[index] > 0):
            self.series['Last Trade Investment'].loc[index] = self.series['CFD Units'].loc[index] * self.series['mid_c'].loc[index]
        else:
            self.series['Last Trade Investment'].loc[index] = self.series['Last Trade Investment'].loc[index-1]
        return self.series['Last Trade Investment']





    def simulate(self):
        end_cash = 0
        number_of_long_trades = 0
        number_of_short_trades = 0
        Total_Index_Return = 0
        Total_Strategy_Return = 0
        self.series['long_signal'].loc[0] = 0
        self.series['short_signal'].loc[0] = 0
        self.series['CFD Units'].loc[0] = 0
        self.series['Last Trade Investment'].loc[0] = 0
        self.series['Cash'].loc[0] = self.parameter[0]
        self.series['Long_CFDs_Value'].loc[0] = self.series['mid_c'].loc[0] * self.series['CFD Units'].loc[0]
        self.series['Short_CFDs_value'].loc[0] = (2 * self.series['Last Trade Investment'].loc[0] -
                                                  self.series['CFD Units'].loc[0] * self.series['mid_c'].loc[0]) * \
                                                 self.series['short_signal'].loc[0]
        self.series['Current Portfolio Value'].loc[0] = self.series['Cash'].loc[0] + self.series['Long_CFDs_Value'].loc[
            0] + self.series['Short_CFDs_value'].loc[0]
        if self.series['Last Trade Investment'].loc[0] == 0:
            self.series['Last Trade Profit'].loc[0] = 0
        else:
            self.series['Last Trade Profit'].loc[0] = (self.series['Current Portfolio Value'].loc[0] -
                                                       self.series['Last Trade Investment'].loc[0]) / \
                                                      self.series['Last Trade Investment'].loc[0]
        self.series['Buy'].loc[0] = 0
        self.series['Sell'].loc[0] = 0
        for index in range(1, len(self.series)):
            self.series['Cash'] = self.get_cash(index)
            self.series['CFD Units'] = self.get_CFD_Units(index)
            self.series['Last Trade Investment'] = self.get_Last_Trade_Investment(index)
            self.series['Long_CFDs_Value']



if __name__ == "__main__":
    order_book = pd.read_csv("WR_ORDER_BOOK.CSV")
    MS = Market_Sim(order_book, 100000, '09/04/1995', '09/05/1995')
    CSV_file = MS.simulate()
    CSV_file.to_csv('Market_Sim.csv')
