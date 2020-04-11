import csv
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

import pandas as pd
import numpy as np
from pandas_datareader import data

start_date = '2010-03-30'
end_date = '2020-03-30'
panel_data = data.DataReader('USDRUB=X', 'yahoo', start_date, end_date)

close = panel_data['Close']
close['2016-01-06'] = np.nan
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
close = close.reindex(all_weekdays)
close = close.fillna(method='ffill')

short_rolling_usd = close.rolling(window=10).mean()
long_rolling_usd = close.rolling(window=100).mean()

fig, ax = plt.subplots(figsize=(16, 9))
ax.plot(close.index, close, label='USD')
ax.plot(short_rolling_usd.index, short_rolling_usd, label='10 days SMA')
ax.plot(long_rolling_usd.index, long_rolling_usd, label='100 days SMA')
ax.legend()
plt.show()
