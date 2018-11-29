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


def made_2d(lst):
    new = []
    for i in range(0, len(lst), 2):
        new.append([lst[i], lst[i + 1]])
    return new


def find(info, lst):
    for l in info:
        if set(lst).issubset(set(l)):
            return l


def find_time(info, trip_x, time_s, time_f, x):
    time1, time2 = [], []
    x2 = made_2d(x)
    for i in range(len(trip_x)):
        if trip_x[i] in x2:
            time1.append(find(info, trip_x[i])[4])
            time2.append(find(info, trip_x[i])[5])
    return time1, time2


def define(clusters, xy_s, xy_f):
    xy_s_2 = np.reshape(xy_s, (-1, 2))
    xy_f_2 = np.reshape(xy_f, (-1, 2))
    trips_x = []
    trips_y = []
    for cluster in clusters:
        for coor in cluster:
            if coor in xy_s_2:
                if list(xy_f_2[find_index(xy_s_2, coor)]) in cluster:
                    trips_x.append(
                        [coor[0], xy_f_2[find_index(xy_s_2, coor)][0]])
                    trips_y.append(
                        [coor[1], xy_f_2[find_index(xy_s_2, coor)][1]])
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
    time_s_2, time_f_2 = find_time(info, trip_x, time_s, time_f, x)
    trip_x2 = [item for sublist in trip_x for item in sublist]
    trip_y2 = [item for sublist in trip_y for item in sublist]
    vision(trip_x2, trip_y2, time_s_2, time_f_2)
