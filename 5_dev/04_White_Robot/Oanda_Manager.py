import pandas as pd
import requests
import numpy as np


class Oanda_Manager():

    def __init__(self):
        Account_details = pd.read_csv('Account_details.csv')
        self.Session = requests.session()
        self.API_KEY = Account_details.iloc[:, 1]
        self.Account_ID = Account_details.iloc[:, 2]
        self.Oanda_URL = Account_details.iloc[:, 3]
        self.Header = {'Authorization': f'Bearer {self.API_KEY}'}


    def get_account_instrument(self, instrument_type):
        request = f"{self.Oanda_URL}/accounts/{self.Account_ID}/instruments?instruments={instrument_type}"
        print(request)
        #Instrument_list = self.Session.get(request, params=None, headers=self.Header)
        df = pd.DataFrame.from_dict(Instrument_list)
        return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]






if __name__ == "__main__":
    O_M = Oanda_Manager()
    print(f"{O_M.Oanda_URL}/accounts/{O_M.Account_ID}/instruments")

    #O_M.get_account_instrument("SPX500_USD")
