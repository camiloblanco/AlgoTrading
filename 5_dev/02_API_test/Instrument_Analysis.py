from Instruments import Instrument
import pandas as pd
import plotly.graph_objects as go

class Instrument_Analysis():

    def __init__(self,API_KEY, Account_ID, Oanda_URL, Header):
        self.Instrument = Instrument(API_KEY, Account_ID, Oanda_URL, Header)

    def Simple_moving_average(self, rolling_window,  asset_name, count, granularity):
        candle_data = self.Instrument.fetch_candle_data(asset_name, count, granularity)
        close_price = candle_data['mid_c']
        candle_data['time'] = candle_data['time'].str.replace('T', ' ')
        candle_data['time'] = candle_data['time'].str.replace('Z', '')
        time = candle_data['time']
        return time, close_price.rolling(window=rolling_window).mean()

    def plot_SMA(self, rolling_window,  asset_name, count, granularity):
        candle_data = self.Instrument.fetch_candle_data(asset_name, count, granularity)
        mid_open = candle_data['mid_o']
        mid_high = candle_data['mid_h']
        mid_low = candle_data['mid_l']
        mid_close = candle_data['mid_c']
        Time_14, SMA_Data_14 = self.Simple_moving_average(rolling_window,  asset_name, count, granularity)
        Time_21, SMA_Data_20 = self.Simple_moving_average(20,  asset_name, count, granularity)
        Time_50, SMA_Data_40 = self.Simple_moving_average(40,  asset_name, count, granularity)
        fig = go.Figure(data=[go.Candlestick(x=Time_14,
                                             open=mid_open,
                                             high=mid_high,
                                             low=mid_low,
                                             close=mid_close),
                              go.Scatter(x=Time_14, y=SMA_Data_14, line=dict(color='orange', width=1)),
                              go.Scatter(x=Time_21, y=SMA_Data_20, line=dict(color='green', width=1)),
                              go.Scatter(x=Time_50, y=SMA_Data_40, line=dict(color='red', width=1))
                              ])
        return fig




if __name__ == "__main__":
    Ins = Instrument_Analysis("fcd13b16706c8b961be0641aebd0f143-285a7112c2a5ec5c8ecd2082de590867", "101-004-19105515-001", "https://api-fxpractice.oanda.com/v3",
                            {'Authorization': f'Bearer {"fcd13b16706c8b961be0641aebd0f143-285a7112c2a5ec5c8ecd2082de590867"}'})
    time, avg = (Ins.Simple_moving_average(12,"SPX500_USD", 1000, "D"))
    fig = (Ins.plot_SMA(12,"SPX500_USD", 1000, "H4"))
    fig.update_layout(
        title="Moving_Averages",
        xaxis_title="Time",
        yaxis_title="close_price",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        ))
    fig.show()

