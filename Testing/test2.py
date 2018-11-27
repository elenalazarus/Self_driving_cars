import numpy as np
import pandas as pd
import chartify

data = pd.DataFrame({'time': pd.date_range('2015-01-01', '2018-01-01')})
n_days = len(data)
data['1st'] = np.array(list(range(n_days))) + np.random.normal(
    0, 10, size=n_days)
data['2nd'] = np.array(list(range(n_days))) + np.random.normal(
    0, 10, size=n_days) + 200
data['3rd'] = np.array(list(range(n_days))) + np.random.normal(
    0, 10, size=n_days) + 500
data['4th'] = np.array(list(range(n_days))) + np.random.normal(
    0, 10, size=n_days) + 700
data['5th'] = np.array(list(range(n_days))) + np.random.normal(
    0, 10, size=n_days) + 800
data['6th'] = np.array(list(range(n_days))) + np.random.normal(
    0, 10, size=n_days) + 1000
print(data)
data = pd.melt(
    data,
    id_vars=['time'],
    value_vars=data.columns[1:],
    value_name='y',
    var_name=['grouping'])

print(data)

# Plot the data
ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
ch.style.set_color_palette(palette_type='sequential')
ch.plot.line(
    data_frame=data.sort_values('time'),
    x_column='time',
    y_column='y',
    color_column='grouping')
ch.set_title("Sequential color palette type")
ch.set_subtitle("Palette type for sequential ordered dimensions")
ch.show('html')
