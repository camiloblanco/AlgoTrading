from Account import Account
from requests import post
import json

class Order(Account):

    def __init__(self, API_KEY, Account_ID, Oanda_URL, Header, data):
        super().__init__(API_KEY, Account_ID, Oanda_URL, Header)
        self.order_data = data

    def create_Account_order(self):

        Order_data = json.dumps(self.order_data)
        account_order = f"{self.Oanda_URL}/accounts/{self.Account_ID}/orders"
        Order_response = post(account_order, headers=self.Header, data=Order_data)
        return Order_response.json()

    def get_unique_asset_order(self):
        unique_account_order = f"{self.Oanda_URL}/accounts/{self.Account_ID}/orders?instrument=EUR_CAD"
        unique_account_response = self.session.get(unique_account_order,params = None, headers=self.Header)
        return unique_account_response.json()








if __name__ == "__main__":

    Order = Order("fcd13b16706c8b961be0641aebd0f143-285a7112c2a5ec5c8ecd2082de590867", "101-004-19105515-001", "https://api-fxpractice.oanda.com/v3", {"Content-Type": "application/json",'Authorization': f'Bearer {"fcd13b16706c8b961be0641aebd0f143-285a7112c2a5ec5c8ecd2082de590867"}'}
                  ,data = {"order": {"units": 10, "instrument": "EUR_CAD", "timeInForce": "FOK", "type": "MARKET", "positionFill": "DEFAULT"}})
    Order.create_Account_order()
    print(Order.get_unique_asset_order())




