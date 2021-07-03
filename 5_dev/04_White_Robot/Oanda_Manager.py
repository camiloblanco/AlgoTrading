import requests
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date
from datetime import timedelta
#import tables as tb
#from tables import *
#from Asset_Table import Asset_Table_Description


# Class to manage the CRUD for OANDA API

class Oanda_Manager():

    # Methods to manage the account

    # Constructors
    def __init__(self,
                 Account_details_file):  # initializes the class Onada_API and create the session method upon intialization
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

    # Merges the candle data from inception till current date on a specific asset by dates
    def get_all_candles_data(self, asset_name, granularity, starting_date, end_date):
        start_date = pd.date_range(starting_date, end_date, freq='AS').tolist()
        end_date = pd.date_range(starting_date, end_date, freq='A').tolist()
        end_date.append(date.today() - timedelta(days = 1))
        starting_idx = 0
        Merged_candle_Dataframe = pd.DataFrame()
        while starting_idx < len(start_date):
            candle_data = self.get_candles_dates(asset_name, granularity, start_date[starting_idx],
                                                 end_date[starting_idx])
            Merged_candle_Dataframe = Merged_candle_Dataframe.append(candle_data)
            starting_idx += 1
            #print(starting_idx)

        # self.create_HDF_table(Merged_candle_Dataframe, "Merged_Candle_Data_H5")
        return Merged_candle_Dataframe

    # Saves a CSV file for  data of a certain asset class
    def save_CSV_file(self, pandas_Dataframe, csv_file_name):
        pandas_Dataframe.to_csv(csv_file_name)

    # Creates HDF Tables for  data of a certain asset class
    #def create_HDF_table(self, Merged_candle_Dataframe, h5_file_name):

      #  Merged_Candle_Data_H5 = tb.open_file(h5_file_name, mode='w', title='Candle_PyTable')
      #  Candle_group = Merged_Candle_Data_H5.create_group('/', 'candledata', 'Candle Date')
      #  Candle_Table = Merged_Candle_Data_H5.create_table(Candle_group, 'candletable', Asset_Table_Description,
                                                          #'Candle Pytable')
      #  Candle_row = Candle_Table.row
      #  Candle_Time = Merged_candle_Dataframe.index.to_list()
      #  [date_obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ') for date_obj in Candle_Time]
      #  Merged_candle_Dataframe = Merged_candle_Dataframe.reset_index()
      #  for idx in range(len(Merged_candle_Dataframe)):
       #     Candle_row['time'] = Candle_Time[idx]
       #    Candle_row['volume'] = Merged_candle_Dataframe['volume'].loc[idx]
       #     Candle_row['mid_o'] = Merged_candle_Dataframe['mid_o'].loc[idx]
       #     Candle_row['mid_h'] = Merged_candle_Dataframe['mid_h'].loc[idx]
       #     Candle_row['mid_l'] = Merged_candle_Dataframe['mid_l'].loc[idx]
       #     Candle_row['mid_c'] = Merged_candle_Dataframe['mid_c'].loc[idx]
       #     Candle_row['bid_o'] = Merged_candle_Dataframe['bid_o'].loc[idx]
       #     Candle_row['bid_h'] = Merged_candle_Dataframe['bid_h'].loc[idx]
       #     Candle_row['bid_l'] = Merged_candle_Dataframe['bid_l'].loc[idx]
       #     Candle_row['bid_c'] = Merged_candle_Dataframe['bid_c'].loc[idx]
       #     Candle_row['ask_o'] = Merged_candle_Dataframe['ask_o'].loc[idx]
       #     Candle_row['ask_h'] = Merged_candle_Dataframe['ask_h'].loc[idx]
       #     Candle_row['ask_l'] = Merged_candle_Dataframe['ask_l'].loc[idx]
       #     Candle_row['ask_c'] = Merged_candle_Dataframe['ask_c'].loc[idx]
       #     Candle_row.append()

        # Candle_Table.flush()
        # Merged_Candle_Data_H5.close()