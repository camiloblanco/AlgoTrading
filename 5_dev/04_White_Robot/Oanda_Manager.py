import pandas as pd
import requests
import numpy as np


class Oanda_Manager():

    def __init__(self):
        Account_details = pd.read_csv('Account_details.csv')
        Account_details_cols = Account_details.columns.tolist()
        print(Account_details_cols)
        Account_details['Account_Name'] = pd.Series(Account_details['Account_Name'], dtype="string")
        print(Account_details['Account_Name'])
        #Account_details.to_dict('records')
        #for i in Account_details:
         #   print(str(i, Account_details[i]))
        self.API_KEY = str(Account_details.iloc[:, 1])
        self.Account_ID = str(Account_details.iloc[:, 2])
        self.Oanda_URL = Account_details.iloc[:, 3]
        self.Header = {'Authorization': f'Bearer {self.API_KEY}'}

    def __repr__(self):
          return str(vars(self))


    def get_account_instrument(self, instrument_type):
        request = f"{self.Oanda_URL}/accounts/{self.Account_ID}/instruments?instruments={instrument_type}"
        print(request)
        #Instrument_list = self.Session.get(request, params=None, headers=self.Header)
        df = pd.DataFrame.from_dict(Instrument_list)
        return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]






if __name__ == "__main__":
    O_M = Oanda_Manager()
    print(O_M.API_KEY)


    #O_M.get_account_instrument("SPX500_USD")
