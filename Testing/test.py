import numpy as np
import pandas as pd
import chartify
#
# # Generate example data
# data = chartify.examples.example_data()
#
# # Plot the data
# ch = chartify.Chart(blank_labels=True, x_axis_type='datetime')
# ch.plot.scatter(
#     data_frame=data,
#     x_column='date',
#     y_column='unit_price')
# ch.set_title("Scatterplot")
# ch.set_subtitle("Plot two numeric values.")
# ch.show('html')

# print(chartify.color_palettes.show())

    # Generate example data
data = pd.DataFrame({'x': list(range(100))})
data['y'] = data['x'] * np.random.normal(size=100)
data['z'] = np.random.choice([2, 4, 5], size=100)
data['country'] = np.random.choice( ['US', 'GB', 'CA', 'JP', 'BR'], size=100)
print(data)

    # Plot the data
ch = chartify.Chart(blank_labels=True)
ch.style.set_color_palette(palette_type='All colors')
ch.plot.scatter(
        data_frame=data,
        x_column='x',
        y_column='y',
        color_column='country')
ch.set_title("Categorical color palette type")
ch.set_subtitle(
        "Default palette type. Use to differentiate categorical series.")
ch.show('html')