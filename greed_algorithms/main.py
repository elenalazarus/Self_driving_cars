from data.reading import reading, reading_2
from objects.car import Car
import numpy


def distance(trip):
    n = 0
    trip_start, trip_finish = [trip.start_x, trip.start_y], [trip.finish_x,
                                                             trip.finish_y]
    n += abs(trip_finish[0] - trip_start[0]) + abs(
        trip_finish[1] - trip_start[1])
    return n


def get_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def count_m(car, trip):
    time = car.time + get_distance(car.position,
                                   (trip.start_x, trip.start_y)) + \
           max(0, trip.earliest - car.time) + get_distance(
        (trip.start_x, trip.start_y), (trip.finish_x, trip.finish_y))
    return time - car.time


def average(trips):
    x = [trip.start_x for trip in trips]
    y = [trip.start_y for trip in trips]
    return numpy.mean(x), numpy.mean(y)


def count_points(car, trip, bonus, middle):
    distance_trip = distance(trip)
    go_distance = get_distance(car.position, (trip.start_x, trip.start_y))
    wait = max(0, trip.earliest - (car.time + go_distance))
    good_time = go_distance + car.time <= trip.earliest
    middle_dist = get_distance((trip.finish_x, trip.finish_y), middle)

    return distance_trip - go_distance - wait + (
        bonus if good_time else 0) - middle_dist


def choose_trip(car, trips, time, bonus):
    all_trips = dict()
    for trip in trips:
        all_trips[trip.id] = count_m(car, trip)
    middle = average(trips)

    possible_trips = filter(lambda trip: trip.car is None, trips)
    possible_trips = filter(lambda r: all_trips[r.id] < (time - car.time),
                            possible_trips)
    possible_trips = filter(
        lambda r: car.time + all_trips[r.id] <= r.latest, possible_trips)
    possible_trips = sorted(list(possible_trips),
                            key=lambda r: count_points(car, r, bonus, middle),
                            reverse=True)
    if len(possible_trips) > 0:
        return possible_trips[0]


def characterize_car(car, trips, time, bonus, waiting):
    trip = choose_trip(car, trips, time, bonus)
    if trip is None:
        return None
    trip.car = car
    car.trips.append(trip)
    meters = count_m(car, trip)
    car.time += meters
    car.position = (trip.finish_x, trip.finish_y)
    waiting.append((car, meters))
    return trip


def write_in_file(path, cars):
    with open(path, 'w') as f:
        for car in cars:
            f.write('{} '.format(len(car.trips)))
            for trip in car.trips:
                f.write('{} '.format(trip.id))
            f.write('\n')


if __name__ == '__main__':
    data = reading(
        '/Users/zlatahayvoronska/Documents/Algorithms/Ad fontes/Self_driving_cars/qualification_round_2018/b_should_be_easy.in')
    trips, rows, cols, n_vehicles, bonus, time = reading_2(data)
    cars = [Car(i + 1) for i in range(n_vehicles)]
    waiting = []
    for car in cars:
        characterize_car(car, trips, time, bonus, waiting)

    n = 0
    while len(waiting) > 0:
        waiting = sorted(waiting, key=lambda x: x[1])
        car, wait_time = waiting[0]
        waiting.pop(0)
        characterize_car(car, trips, time, bonus, waiting)
        if n % 10 == 0: print('{} rides in queue'.format(len(waiting)))
        n += 1

    write_in_file('result.txt', cars)


