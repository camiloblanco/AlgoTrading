import pandas as pd
import requests
import numpy as np


class Oanda_Manager():

    def __init__(self):
        Account_details = pd.read_csv('Account_details.csv', dtype="string")
        self.Session = requests.session()
        self.API_KEY = (Account_details.iloc[:, 1]).str.cat(sep='\n')
        self.Account_ID = (Account_details.iloc[:, 2]).str.cat(sep='\n')
        self.Oanda_URL = (Account_details.iloc[:, 3]).str.cat(sep='\n')
        self.Header = {'Authorization': f'Bearer {self.API_KEY}'}

    def __repr__(self):
          return str(vars(self))


    def get_account_instrument(self, instrument_type):
        request = f"{self.Oanda_URL}/accounts/{self.Account_ID}/instruments?instruments={instrument_type}"
        data = self.Session.get(request, params=None, headers=self.Header)
        instrument = data['instruments']
        return df
        #return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]






if __name__ == "__main__":
    O_M = Oanda_Manager()
    print(O_M.get_account_instrument("SPX500_USD"))


    #O_M.get_account_instrument("SPX500_USD")
