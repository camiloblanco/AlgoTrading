from tables import *
import tables as tb   # but in this tutorial we use "from tables import \*"
import numpy as np

class Candle_Data_Types(tb.IsDescription):
    time = tb.StringCol(25)# 16-character String
    volume = tb.Int64Col()  # Signed 64-bit integer
    mid_o = tb.Float64Col()  # Unsigned short integer
    mid_h = tb.Float64Col()  # unsigned byte
    mid_l = tb.Float64Col()  # 32-bit integer
    mid_c = tb.Float64Col()  # 32-bit integer
    bid_o = tb.Float64Col()  # float  (single-precision)
    bid_h = tb.Float64Col()
    bid_l = tb.Float64Col()
    bid_c = tb.Float64Col()
    ask_o = tb.Float64Col()
    ask_h = tb.Float64Col()
    ask_l = tb.Float64Col()
    ask_c = tb.Float64Col()
