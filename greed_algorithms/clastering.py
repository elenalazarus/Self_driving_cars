from data.reading import reading
from data.reading import get_coordinates
from Visualize.visualize import vision
from math import sqrt
import numpy as np


def min_distance(av_p, point):
    distances = []
    for a in av_p:
        distances.append(sqrt((a[0] - point[0]) ** 2 + (a[1] - point[1]) ** 2))
    return distances.index(min(distances))


def find_index(lst, element):
    n = 0
    for e in lst:
        if set(e) == set(element):
            return n
        n += 1


def find_time(trip_x, info):
    time_s, time_f = [], []
    for i in range(len(trip_x)):
        if set(list((info[i][0], info[i][2]))) in set(trip_x[i]):
            time_s.append(info[i][4])
            time_f.append(info[i][5])
    return time_s, time_f


def define(clasters, xy_s, xy_f):
    xy_s_2 = np.reshape(xy_s, (-1, 2))
    xy_f_2 = np.reshape(xy_f, (-1, 2))
    trips_x = []
    trips_y = []
    for claster in clasters:
        for coor in claster:
            if coor in xy_s_2:
                if list(xy_f_2[find_index(xy_s_2, coor)]) in claster:
                    trips_x.append(
                        [coor[0], xy_f_2[find_index(xy_s_2, coor)][0]])
                    trips_y.append(
                        [coor[1], xy_f_2[find_index(xy_s_2, coor)][1]])
            else:
                if list(xy_s_2[find_index(xy_f_2, coor)]) in claster:
                    trips_x.append(
                        [coor[0], xy_s_2[find_index(xy_f_2, coor)][0]])
                    trips_y.append(
                        [coor[1], xy_s_2[find_index(xy_f_2, coor)][1]])
    return trips_x, trips_y


def clastering(info, x, y):
    average_points = []
    average_points.append([info[0][0] * 1 / 4, info[0][1] * 1 / 4])
    average_points.append([info[0][0] * 1 / 4, info[0][1] * 3 / 4])
    average_points.append([info[0][0] * 3 / 4, info[0][1] * 1 / 4])
    average_points.append([info[0][0] * 3 / 4, info[0][1] * 3 / 4])
    clasters = [[], [], [], []]
    for i in range(len(x)):
        ind = min_distance(average_points, [x[i], y[i]])
        clasters[ind].append([x[i], y[i]])
    return clasters


if __name__ == '__main__':
    info = reading(
        '/Users/zlatahayvoronska/Documents/Algorithms/Ad fontes/Self_driving_cars/qualification_round_2018/b_should_be_easy.in')
    x, y, time_s, time_f, xy_s, xy_f = get_coordinates(info)
    info.sort(key=lambda x: x[4])
    clasters = clastering(info, x, y)
    trip_x, trip_y = define(clasters, xy_s, xy_f)
    time_s_2, time_f_2 = find_time(trip_x, info)
    # vision(trip_x, trip_y, time_s_2, time_f_2)
