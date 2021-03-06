import pandas as pd
import util
from Account import Account


class Instrument(Account):

    def __init__(self, API_KEY, Account_ID, Oanda_URL, Header):
        super().__init__(API_KEY, Account_ID, Oanda_URL, Header)

    @staticmethod
    def reformat_file(json_response):
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


    def __repr__(self):
        return str(vars(self))

    def get_instruments_data(self):
        status_code, data = self.account_instruments()
        instruments = data['instruments']
        return instruments

    def get_instruments_list(self):
        instrument_list = self.get_instruments_data()
        print(instrument_list)
        df = pd.DataFrame.from_dict(instrument_list)
        print(df)
        return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]


    def fetch_candle_data(self, asset_name, count, granularity):
        candle_data_url = f"{self.Oanda_URL}/instruments/{asset_name}/candles"
        params = dict(count=count, granularity=granularity, price="MBA")
        candle_response = self.session.get(candle_data_url, params=params, headers=self.Header)
        candle_dataframe = self.reformat_file(candle_response.json())
        return candle_dataframe

    #For Forex Data
    def fetch_order_book(self, asset_name):
        order_data_url = f"{self.Oanda_URL}/instruments/{asset_name}/orderBook"
        order_response = self.session.get(order_data_url, params = None, headers = self.Header)
        return order_response.json()

    #For Forex Data
    def fetch_position_book(self, asset_name):
        position_data_url = f"{self.Oanda_URL}/instruments/{asset_name}/positionBook"
        position_response = self.session.get(position_data_url, params=None, headers=self.Header)
        return position_response.json()



if __name__ == "__main__":
    Instrument = Instrument("fcd13b16706c8b961be0641aebd0f143-285a7112c2a5ec5c8ecd2082de590867", "101-004-19105515-001", "https://api-fxpractice.oanda.com/v3",
                            {'Authorization': f'Bearer {"fcd13b16706c8b961be0641aebd0f143-285a7112c2a5ec5c8ecd2082de590867"}'})
    print(Instrument.get_instruments_list())


