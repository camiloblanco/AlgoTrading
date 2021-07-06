from tables import *
import tables as tb  # but in this tutorial we use "from tables import \*"
import numpy as np


class Asset_Table_Description(tb.IsDescription):
    time = tb.StringCol(24, pos=0)  # 16-character String
    volume = tb.Int64Col(pos=1)  # Signed 64-bit integer
    mid_o = tb.Float64Col(pos=2)  # Unsigned short integer
    mid_h = tb.Float64Col(pos=3)  # unsigned byte
    mid_l = tb.Float64Col(pos=4)  # 32-bit integer
    mid_c = tb.Float64Col(pos=5)  # 32-bit integer
    bid_o = tb.Float64Col(pos=6)  # float  (single-precision)
    bid_h = tb.Float64Col(pos=7)
    bid_l = tb.Float64Col(pos=8)
    bid_c = tb.Float64Col(pos=9)
    ask_o = tb.Float64Col(pos=10)
    ask_h = tb.Float64Col(pos=11)
    ask_l = tb.Float64Col(pos=12)
    ask_c = tb.Float64Col(pos=13)
