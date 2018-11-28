import pandas as pd
import chartify
from data.reading import reading
from data.reading import get_coordinates


def vision(x, y, time_s, time_f):
    data = pd.DataFrame({'x': x})
    data['y'] = [i for i in y]
    difference = []
    lst = []
    data['color'] = [val for val in range(1, len(x) // 2 + 1) for _ in (0, 1)]
    data['time_s'] = [val for val in time_s for _ in (0, 1)]
    data['time_f'] = [val for val in time_f for _ in (0, 1)]
    for i in range(len(time_s)):
        difference.extend([time_f[i] - time_s[i], time_f[i] - time_s[i]])

    border = max(difference) // 60

    for i in difference:
        ind = i // border
        lst.append(ind)
    data['diff'] = [i for i in lst]

    data['x_s'] = [x[i] for i in range(len(x)) if i % 2 == 0 for _ in (0, 1)]
    data['x_f'] = [x[i] for i in range(len(x)) if i % 2 != 0 for _ in (0, 1)]
    data['y_s'] = [y[i] for i in range(len(y)) if i % 2 == 0 for _ in (0, 1)]
    data['y_f'] = [y[i] for i in range(len(y)) if i % 2 != 0 for _ in (0, 1)]

    print(data)

    ch = chartify.Chart(blank_labels=True)
    ch.style.set_color_palette(palette_type='diverging')

    ch.plot.line(
        data_frame=data,
        x_column='x',
        y_column='y',
        line_width=1,
        color_column='time_f')

    ch.plot.scatter(
        data_frame=data,
        x_column='x_s',
        y_column='y_s',
        marker='square',
        size_column='diff',
        color_column='time_f')

    ch.plot.scatter(
        data_frame=data,
        x_column='x_f',
        y_column='y_f',
        marker='circle',
        size_column='diff',
        color_column='time_f')

    ch.set_title("Map of the city")
    ch.set_subtitle("Ways for cars to go.")
    ch.show('html')


if __name__ == '__main__':
    data = reading(
        '/Users/zlatahayvoronska/Documents/Algorithms/Ad fontes/Self_driving_cars/qualification_round_2018/b_should_be_easy.in')
    x, y, time_s, time_f, xy_s, xy_f = get_coordinates(data)
    vision(x, y, time_s, time_f)
