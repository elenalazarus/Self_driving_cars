import numpy as np
import pandas as pd
import chartify

# Generate example data
data = pd.DataFrame({'x': list(range(100))})
data['y'] = data['x'] * np.random.normal(size=100)
data['z'] = np.random.choice([2, 4, 5], size=100)
data['country'] = np.random.choice(
    ['US', 'GB', 'CA', 'JP', 'BR'], size=100)

print(data)

# Plot the data
ch = chartify.Chart(blank_labels=True)
ch.plot.scatter(
    data_frame=data,
    x_column='x',
    y_column='y',
    size_column='z',
    color_column='country')
ch.set_title(
    'ch.show(): Faster rendering with HTML. Recommended while drafting.')
ch.set_subtitle('No watermark. Does not display on github.')
ch.show('html')  # Show with HTML

ch.set_title(
    'ch.show("png"): Return a png file for easy copying into slides')
ch.set_subtitle('Will display on github.')
ch.show('png')  # Show with PNG
