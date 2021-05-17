import requests
import pandas as pd

# Class to manage the CRUD for OANDA API
class Oanda_Manager():
    
    #Constructors
    def __init__(self, Account_details_file): #initializes the class Onada_API and create the session method upon intialization
        account = pd.read_csv(Account_details_file)
        self.session = requests.Session()
        self.API_KEY = account.iloc[0, 0]
        self.Account_ID = account.iloc[0, 1]
        self.Oanda_URL = account.iloc[0, 2]
        self.Header = {'Authorization': f'Bearer {self.API_KEY}'}
        
    # Methods to manage the account

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



    def account_summary(self):
        account_summary = f"{self.Oanda_URL}/accounts/{self.Account_ID}/summary"
        response = self.session.get(account_summary, params=None, headers=self.Header)
        return response.status_code, response.json()


    def account_changes(self, Transaction_ID):
        account_changes = f"{self.OANDA_URL}/accounts/{self.Account_ID}/changes sinceTransactionID =" + Transaction_ID
        response = self.session.get(account_changes, params=None, headers=self.Header)
        return response.status_code, response.json()

if __name__ == "__main__":
    O_M = Oanda_Manager()
    print(O_M.get_account_instrument("SPX500_USD"))


    #O_M.get_account_instrument("SPX500_USD")
