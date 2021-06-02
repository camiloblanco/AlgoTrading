import numpy as np
import pandas as pd
from scipy.stats import linregress


class White_Strategy():

    def __init__(self, csv_filename):
        self.series = pd.read_csv(csv_filename)


    def moving_avg_strategy(self):
        pass



    