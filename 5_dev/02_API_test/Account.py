import requests
import pandas as pd
import util



class Account():

    def __init__(self, API_KEY, Account_ID, Oanda_URL, Header): #initializes the class Onada_API and create the session method upon intialization
        self.session = requests.Session()
        self.API_KEY = API_KEY
        self.Account_ID = Account_ID
        self.Oanda_URL = Oanda_URL
        self.Header = Header


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
        account_changes = f"{self.OANDA_URL}/accounts/{self.Account_ID}/changes?sinceTransactionID =" + Transaction_ID
        response = self.session.get(account_changes, params=None, headers=self.Header)
        return response.status_code, response.json()

    def account_patch(self,Patch):
        Patch_data = json.dumps(self.order_data)





if __name__ == '__main__':
    acc = Account("fcd13b16706c8b961be0641aebd0f143-285a7112c2a5ec5c8ecd2082de590867", "101-004-19105515-001", "https://api-fxpractice.oanda.com/v3",
                            {'Authorization': f'Bearer {"fcd13b16706c8b961be0641aebd0f143-285a7112c2a5ec5c8ecd2082de590867"}'})
    print(acc.account_summary())


