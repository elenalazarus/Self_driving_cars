import pandas as pd
import chartify
from data.reading import reading


def vision(x, y, time_s, time_f):
    data = pd.DataFrame({'x': x})
    data['y'] = [i for i in y]
    lst = []
    lst2 = []
    lst3 = []
    lst4 = []
    lst5 = []
    for i in range(1, len(x) // 2 + 1):
        lst.extend([i, i])
    data['color'] = [str(i) for i in lst]
    for i in time_s:
        lst2.extend([i, i])
    for i in time_f:
        lst3.extend([i, i])
    data['time_s'] = [i for i in lst2]
    data['time_f'] = [i for i in lst3]

    for i in range(len(time_s)):
        lst4.extend([time_f[i] - time_s[i], time_f[i] - time_s[i]])

    border = max(lst4) // 60


    for i in lst4:
        ind = i // border
        lst5.append(ind)

    data['diff'] = [i for i in lst5]

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
        x_column='x',
        y_column='y',
        marker='hex',
        size_column='diff',
        color_column='time_f')

    ch.set_title("Map of the city")
    ch.set_subtitle("Ways for cars to go.")
    ch.show('html')


def get_coordinates(data):
    x = []
    y = []
    time_s = []
    time_f = []
    for trip in data[1:len(data) // 10]:
        x.extend([trip[0], trip[2]])
        y.extend([trip[1], trip[3]])
        time_s.append(trip[4])
        time_f.append(trip[5])
    return x, y, time_s, time_f






if __name__ == '__main__':
    data = reading('b_should_be_easy.in')
    x, y, time_s, time_f = get_coordinates(data)
    vision(x, y, time_s, time_f)
