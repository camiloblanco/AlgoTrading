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
        self.Bearer = {
            'Authorization': f'Bearer {self.API_KEY}'
        }

    def get_account_instrument(self, instrument_type):
        instrument_list = f"{self.Oanda_URL}/accounts/{self.Account_ID}/instruments?instruments={instrument_type}"
        print(instrument_list)
        df = pd.DataFrame.from_dict(instrument_list)
        return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]




def get_account_instrument(self, instrument_type):
    pass


if __name__ == "__main__":
    O_M = Oanda_Manager()
    O_M.get_account_instrument("SPX500_USD")
