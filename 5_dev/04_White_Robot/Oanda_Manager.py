import requests
import pandas as pd

# Class to manage the CRUD for OANDA API
class Oanda_Manager():
    
    #Constructors
        
    def __init__(self, API_KEY, Account_ID, Oanda_URL, Header): #initializes the class Onada_API and create the session method upon intialization
        self.session = requests.Session()
        self.API_KEY = API_KEY
        self.Account_ID = Account_ID
        self.Oanda_URL = Oanda_URL
        self.Header = Header
        
    #Methods to manage the account

    def account_list(self):
        account_url = f"{self.Oanda_URL}/accounts"
        response = self.session.get(account_url, params=None, headers=self.Header)
        return response.status_code, response.json()

    def account_id(self):
        account_id = f"{self.Oanda_URL}/accounts/{self.Account_ID}"
        response = self.session.get(account_id, params=None, headers=self.Header)
        return response.status_code, response.json()

    def account_summary(self):
        account_summary = f"{self.Oanda_URL}/accounts/{self.Account_ID}/summary"
        response = self.session.get(account_summary, params=None, headers=self.Header)
        return response.status_code, response.json()

    def account_instruments(self):
        instruments = f"{self.Oanda_URL}/accounts/{self.Account_ID}/instruments"
        print(instruments)
        response = self.session.get(instruments, params=None, headers=self.Header)
        return response.status_code, response.json()

    def account_changes(self, Transaction_ID):
        account_changes = f"{self.OANDA_URL}/accounts/{self.Account_ID}/changes sinceTransactionID =" + Transaction_ID
        response = self.session.get(account_changes, params=None, headers=self.Header)
        return response.status_code, response.json()

    def account_patch(self,Patch):
        Patch_data = json.dumps(self.order_data)
        
    #Methods to read and format instruments
    
    #This method formats the candle data in a dataframe
    def format_candles(self,json_response):
        prices = ['mid', 'bid', 'ask']
        ohlc = ['o', 'h', 'l', 'c']
        our_data = []
        for candle in json_response['candles']:
            if candle['complete'] == False:
                continue
            new_dict = {'time': candle['time'], 'volume': candle['volume']}
            for price in prices:
                for oh in ohlc:
                    new_dict[f"{price}_{oh}"] = candle[price][oh]
            our_data.append(new_dict)
        return pd.DataFrame.from_dict(our_data)
    
    # Method that read the candle data from Oanda API for specific asset
    def read_instrument_candles(self, asset_name, count, granularity):
        candle_data_url = f"{self.Oanda_URL}/instruments/{asset_name}/candles"
        params = dict(count=count, granularity=granularity, price="MBA")
        candle_response = self.session.get(candle_data_url, params=params, headers=self.Header)
        candle_dataframe = self.format_candles(candle_response.json())
     
        return candle_dataframe
        
        
