from os import stat
import numpy as np
from scipy import stats
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime as dt
from threading import Thread


def data_generation(data_set_size):

    x_data = []
    x_data = np.arange(0, data_set_size, 1)
    y_data = []
    y_data = stats.norm.pdf(x_data, data_set_size/2, 1 + data_set_size/5)

    x_timestamps = []
    datetime = dt.datetime.now()
    for i in x_data.tolist():

        z = datetime + dt.timedelta(milliseconds=i*10)
        x_timestamps.append(z.isoformat())

    df = pd.DataFrame({'time': x_timestamps, 'bar': y_data},
                      index=None)
    df.to_csv(
        os.path.abspath(f"./data/{data_set_size}-data.csv"), index=False)


o = [100, 1000, 10000, 100000, 1000000, 10000000, 100000000]

for i in o:

    Thread(target=data_generation, args=(i,)).start()
