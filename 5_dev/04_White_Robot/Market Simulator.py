
import numpy as np
import pandas as pd

class Market_Sim():
    def __init__(self, csv_filename, initial_cash, start_date, end_date):
        self.series = csv_filename
        self.initial_cash = initial_cash
        self.start_date = start_date
        self.end_date = end_date
