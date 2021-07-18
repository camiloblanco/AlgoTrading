import numpy as np
import pandas as pd


class Market_Sim:
    def __init__(self, csv_filename, initial_cash):
        self.parameter = [initial_cash]
        self.series = csv_filename
        self.initial_cash = initial_cash
        self.series['Cash'] = np.nan
        self.series['CFD Units'] = np.nan
        self.series['Last Trade Investment'] = np.nan
        self.series['Long_CFDs_Value'] = np.nan
        self.series['Short_CFDs_Value'] = np.nan
        self.series['Intrinsic_Value'] = np.nan
        self.series['Portfolio Value'] = np.nan
        self.series['Last Trade Profit'] = np.nan
        self.series['Index Trade Profit'] = np.nan
        self.series['Position'] = 0
        self.series['Signals'] = self.series['long_signal'] + self.series['short_signal']

    def get_cash(self, index):
        if (self.series['CFD Units'].loc[index - 1] == 0) and (self.series['CFD Units'].loc[index] > 0):
            self.series['Cash'].loc[index] = 0
        elif (self.series['Last Trade Investment'].loc[index] == 0) and (
                self.series['Last Trade Investment'].loc[index - 1] > 0):
            self.series['Cash'].loc[index] = self.series['Portfolio Value'].loc[index - 1]
        else:
            self.series['Cash'].loc[index] = self.series['Cash'].loc[index - 1]
        return self.series['Cash'].loc[index]

    def get_CFD_Units(self, index):
        if (self.series['long_signal'].loc[index] == 0) and (self.series['short_signal'].loc[index] == 0):
            self.series['CFD Units'].loc[index] = 0
        elif ((self.series['long_signal'].loc[index - 1] == 0) and (self.series['long_signal'].loc[index] == 1)) or \
                ((self.series['short_signal'].loc[index - 1] == 0) and (self.series['short_signal'].loc[index]) == -1):
            self.series['CFD Units'].loc[index] = (self.series['Cash'].loc[index - 1] / self.series['mid_c'].loc[index])
        else:
            self.series['CFD Units'].loc[index] = self.series['CFD Units'].loc[index - 1]
        return self.series['CFD Units'].loc[index]

    def get_Last_Trade_Investment(self, index):
        if (self.series['long_signal'].loc[index] == 0) and (self.series['short_signal'].loc[index] == 0):
            self.series['Last Trade Investment'].loc[index] = 0
        elif (self.series['CFD Units'].loc[index - 1] == 0) and (self.series['CFD Units'].loc[index] > 0):
            self.series['Last Trade Investment'].loc[index] = self.series['CFD Units'].loc[index] * \
                                                              self.series['mid_c'].loc[index]
        else:
            self.series['Last Trade Investment'].loc[index] = self.series['Last Trade Investment'].loc[index - 1]
        return self.series['Last Trade Investment'].loc[index]

    def get_Long_CFDs_Value(self, index):
        self.series['Long_CFDs_Value'].loc[index] = self.series['CFD Units'].loc[index] * self.series['mid_c'].loc[
            index] * self.series['long_signal'].loc[index]
        return self.series['Long_CFDs_Value'].loc[index]

    def get_Short_CFDs_Value(self, index):
        self.series['Short_CFDs_Value'].loc[index] = - (
                2 * self.series['Last Trade Investment'].loc[index] - self.series['CFD Units'].loc[index] *
                self.series['mid_c'].loc[index]) * self.series['short_signal'].loc[index]
        return self.series['Short_CFDs_Value'].loc[index]

    def get_Intrinsic_Value(self, index):
        self.series['Intrinsic_Value'].loc[index] = self.series['Long_CFDs_Value'].loc[index] + \
                                                    self.series['Short_CFDs_Value'].loc[index]
        return self.series['Intrinsic_Value'].loc[index]

    def get_Portfolio_Value(self, index):
        self.series['Portfolio Value'].loc[index] = self.series['Cash'].loc[index] + \
                                                    self.series['Long_CFDs_Value'].loc[index] + \
                                                    self.series['Short_CFDs_Value'].loc[index]
        return self.series['Portfolio Value'].loc[index]

    def get_Last_Trade_Profit(self, index):
        if self.series['Last Trade Investment'].loc[index] == 0:
            self.series['Last Trade Profit'].loc[index] = 0
        else:
            self.series['Last Trade Profit'].loc[index] = (self.series['Portfolio Value'].loc[index] -
                                                           self.series['Last Trade Investment'].loc[index]) / \
                                                          self.series['Last Trade Investment'].loc[index]
        return self.series['Last Trade Profit'].loc[index]

    def get_position(self, index, no_of_long_trades, no_of_short_trades):
        if ((self.series['long_signal'].loc[index - 1] == 0) and (self.series['long_signal'].loc[index] != 0)) or \
                ((self.series['short_signal'].loc[index - 1] == 0) and (self.series['short_signal'].loc[index] != 0)):
            self.series['Position'].loc[index] = 1
            no_of_long_trades += 1
        elif ((self.series['long_signal'].loc[index - 1] != 0) and (self.series['long_signal'].loc[index] == 0)) or \
                ((self.series['short_signal'].loc[index - 1] != 0) and (self.series['short_signal'].loc[index] == 0)):
            self.series['Position'].loc[index] = -1
            no_of_short_trades += 1
        return self.series['Position'].loc[index], no_of_long_trades, no_of_short_trades

    def simulate(self):
        number_of_long_trades = 0
        number_of_short_trades = 0
        self.series['long_signal'].loc[0] = 0
        self.series['short_signal'].loc[0] = 0
        self.series['CFD Units'].loc[0] = 0
        self.series['Last Trade Investment'].loc[0] = 0
        self.series['Cash'].loc[0] = self.parameter[0]
        self.series['Long_CFDs_Value'].loc[0] = self.series['mid_c'].loc[0] * self.series['CFD Units'].loc[0]
        self.series['Short_CFDs_Value'].loc[0] = -(2 * self.series['Last Trade Investment'].loc[0] -
                                                   self.series['CFD Units'].loc[0] * self.series['mid_c'].loc[0]) * \
                                                 self.series['short_signal'].loc[0]
        self.series['Portfolio Value'].loc[0] = self.series['Cash'].loc[0] + self.series['Long_CFDs_Value'].loc[
            0] + self.series['Short_CFDs_Value'].loc[0]
        if self.series['Last Trade Investment'].loc[0] == 0:
            self.series['Last Trade Profit'].loc[0] = 0
        else:
            self.series['Last Trade Profit'].loc[0] = (self.series['Portfolio Value'].loc[0] -
                                                       self.series['Last Trade Investment'].loc[0]) / \
                                                      self.series['Last Trade Investment'].loc[0]
        for index in range(1, len(self.series)):
            self.series['CFD Units'].loc[index] = self.get_CFD_Units(index)
            self.series['Last Trade Investment'].loc[index] = self.get_Last_Trade_Investment(index)
            self.series['Cash'].loc[index] = self.get_cash(index)
            self.series['Long_CFDs_Value'].loc[index] = self.get_Long_CFDs_Value(index)
            self.series['Short_CFDs_Value'].loc[index] = self.get_Short_CFDs_Value(index)
            self.series['Intrinsic_Value'].loc[index] = self.get_Intrinsic_Value(index)
            self.series['Portfolio Value'].loc[index] = self.get_Portfolio_Value(index)
            self.series['Last Trade Profit'].loc[index] = self.get_Last_Trade_Profit(index)
            self.series['Position'].loc[index], number_of_long_trades, number_of_short_trades = self.get_position(index,
                                                                                                                  number_of_long_trades,
                                                                                                                  number_of_short_trades)
            if index % 1000 == 0:
                print(index)
        self.series['Index Returns'] = self.series.mid_c.pct_change(periods=1)
        Total_Strategy_Return = (self.series['Portfolio Value'].loc[len(self.series) - 1] - self.parameter[0]) / self.parameter[0]
        Total_Index_Return = (self.series['Index Returns'].loc[len(self.series) - 1] - self.parameter[0]) / self.parameter[0]
        end_cash = self.series['Cash'].loc[len(self.series) - 1]
        #end_Portfolio_Value = self.series['']
        return self.series, self.parameter, end_cash, number_of_long_trades, number_of_short_trades, Total_Strategy_Return, Total_Index_Return

    def Portfolio_Simulation_csv_outputs(self):
        self.series = self.simulate()
        header = ['time', 'mid_c', 'Signals', 'CFD Units', 'Intrinsic_Value', 'Portfolio Value', 'Last Trade Profit']
        return self.series.to_csv('Portfolio_Simulation.csv', columns=header)

    def Simulation_KPI_csv_outputs(self):
        self.series, self.parameter, end_cash, number_of_long_trades, number_of_short_trades, Total_Strategy_Return, Total_Index_Return = self.simulate()
        KPI_dataframe = pd.DataFrame({'Simulation Parameters': [self.parameter],
                                      'End Cash': [end_cash],
                                      'Number of Long Trades': [number_of_long_trades],
                                      'Number of Short Trades': [number_of_short_trades],
                                      'Total Strategy Returns': [Total_Strategy_Return],
                                      'Total Index Return': [Total_Index_Return]})
        return KPI_dataframe.to_csv('Simulation_KPI.csv')


if __name__ == "__main__":
    order_book = pd.read_csv("WR_ORDER_BOOK.CSV")
    MS = Market_Sim(order_book, 10000)
    MS.Simulation_KPI_csv_outputs()
