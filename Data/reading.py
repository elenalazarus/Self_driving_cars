def reading(path):
    data = []
    with open(path, 'r') as f:
        output = f.read()
        for line in output.split('\n'):
            data.append(list(map(int, line.split())))
    data.pop(-1)
    return data


def get_coordinates(data):
    x = []
    y = []
    xy_s = []
    xy_f = []
    time_s = []
    time_f = []
    for trip in data[1:]:
        x.extend([trip[0], trip[2]])
        y.extend([trip[1], trip[3]])
        xy_s.extend([trip[0], trip[1]])
        xy_f.extend([trip[2], trip[3]])
        time_s.append(trip[4])
        time_f.append(trip[5])
    return x, y, time_s, time_f, xy_s, xy_f
