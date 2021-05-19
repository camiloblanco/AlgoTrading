import requests
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date

# Class to manage the CRUD for OANDA API
class Oanda_Manager():

    # Methods to manage the account

    # Constructors
    def __init__(self, Account_details_file):  # initializes the class Onada_API and create the session method upon intialization
        account = pd.read_csv(Account_details_file)
        self.session = requests.Session()
        self.API_KEY = account.iloc[0, 0]
        self.Account_ID = account.iloc[0, 1]
        self.Oanda_URL = account.iloc[0, 2]
        self.Header = {'Authorization': f'Bearer {self.API_KEY}'}

    # Methods to manage the account

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

    def account_patch(self, Patch):
        pass

    # Methods to read and format instruments

    # This method formats the candle data in a dataframe
    def format_candles(self, json_response):
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
        candle_data = pd.DataFrame.from_dict(our_data)

        # Get the datetime from Oanda date format
        candle_data['time'] = pd.to_datetime(candle_data['time'], format='%Y-%m-%dT%H:%M:%S.%fZ')
        candle_data = candle_data.set_index('time')

        # Cast prices from Oanda text response
        candle_data['volume'] = candle_data['volume'].astype(float)
        cols = candle_data.columns[candle_data.dtypes.eq('object')]
        candle_data[cols] = candle_data[cols].astype(float)

        return candle_data

    # Get the candle data from Oanda API for specific asset by count
    def get_candles_count(self, asset_name, granularity, count):
        candle_data_url = f"{self.Oanda_URL}/instruments/{asset_name}/candles"
        params = dict(price="MBA", granularity=granularity, count=count)
        candle_response = self.session.get(candle_data_url, params=params, headers=self.Header)
        candle_dataframe = self.format_candles(candle_response.json())
        return candle_dataframe

    # Get the candle data from Oanda API for specific asset by dates
    ## Scape from... https://stackoverflow.com/questions/54974442/escape-reserved-keywords-python
    def get_candles_dates(self, asset_name, granularity, from_date, to_date):
        # Convert the datetime to Oanda date format
        from_date = from_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        to_date = to_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        # Make the request
        candle_data_url = f"{self.Oanda_URL}/instruments/{asset_name}/candles"
        params = dict(price="MBA", granularity=granularity, **{'from': from_date}, to=to_date)
        candle_response = self.session.get(candle_data_url, params=params, headers=self.Header)
        candle_dataframe = self.format_candles(candle_response.json())
        return candle_dataframe

    #Merges the candle data from inception till current date on a specific asset by dates
    def get_all_candles_data(self, asset_name, granularity, starting_date, end_date):
        start_date = pd.date_range(starting_date, date.today(), freq='AS').tolist()
        end_date = pd.date_range(starting_date, date.today(), freq='A').tolist()
        end_date.append(date.today())
        starting_idx = 0
        Merged_candle_Dataframe = pd.DataFrame()
        while starting_idx < len(start_date):
            candle_data = self.get_candles_dates(asset_name,granularity,start_date[starting_idx], end_date[starting_idx])
            Merged_candle_Dataframe = Merged_candle_Dataframe.append(candle_data)
            starting_idx += 1
        return Merged_candle_Dataframe

    #Creates HDF Tables for  data of a certain asset class
    



if __name__ == '__main__':
    O_M = Oanda_Manager('Account_details.csv')
    starting_date = pd.to_datetime('2003-01-01')
    to_date = date.today()
    Merged_candle_data = O_M.get_all_candles_data("SPX500_USD", "H4", starting_date, to_date)
    Merged_candle_data.to_csv('Merged_candle_data.csv')


