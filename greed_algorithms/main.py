from data.reading import reading, reading_2
from objects.car import Car
import numpy
import time


def distance(trip):
    '''
    Distance of the trip
    '''
    n = 0
    trip_start, trip_finish = [trip.start_x, trip.start_y], [trip.finish_x,
                                                             trip.finish_y]
    n += abs(trip_finish[0] - trip_start[0]) + abs(
        trip_finish[1] - trip_start[1])
    return n


def get_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def count_m(car, trip):
    '''
    Distance between car and start
    '''
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
    '''
    Profit for trip
    '''
    distance_trip = distance(trip)
    # Car is going to start
    go_distance = get_distance(car.position, (trip.start_x, trip.start_y))
    # Car is waiting
    wait = max(0, trip.earliest - (car.time + go_distance))
    # We have a bonus
    good_time = go_distance + car.time <= trip.earliest
    # Are we in city centre?
    middle_dist = get_distance((trip.finish_x, trip.finish_y), middle)
    return distance_trip - go_distance - wait + (
        bonus if good_time else 0) - middle_dist


def choose_trip(car, trips, time, bonus, indicator):
    all_trips = dict()
    for trip in trips:
        # Dict with car and distance of trips
        all_trips[trip.id] = count_m(car, trip)
    middle = average(trips)

    # Not finished rides
    possible_trips = filter(lambda trip: trip.car is None, trips)

    # To be in time
    possible_trips = filter(
        lambda trip: all_trips[trip.id] < (time - car.time),
        possible_trips)

    # Not too late
    possible_trips = filter(
        lambda trip: car.time + all_trips[trip.id] <= trip.latest,
        possible_trips)

    # Not too early
    possible_trips = filter(
        lambda trip: car.time + all_trips[trip.id] >= trip.earliest,
    possible_trips)

    # Which algorithm?
    if indicator == 1:
        possible_trips = variant_1(possible_trips, middle, bonus)

    elif indicator == 2:
        possible_trips = variant_2(possible_trips)

    elif indicator == 3:
        possible_trips = variant_3(possible_trips)

    if len(possible_trips) > 0:
        return possible_trips[0]


def variant_1(possible_trips, middle, bonus):
    '''
    Sort for profit
    '''
    possible_trips = sorted(list(possible_trips),
                            key=lambda trip: count_points(car, trip, bonus,
                                                          middle),
                            reverse=True)
    return possible_trips


def variant_2(possible_trips):
    '''
    Sort for nearest start
    '''
    possible_trips = sorted(list(possible_trips),
                            key=lambda trip: trip.earliest)

    return possible_trips


def variant_3(possible_trips):
    possible_trips = sorted(list(possible_trips),
                            key=lambda trip: trip.latest)
    return possible_trips


def characterize_car(car, trips, time, bonus, waiting, indicator):
    trip = choose_trip(car, trips, time, bonus, indicator)
    if trip is None:
        return None
    distance_trip = distance(trip)
    go_distance = get_distance(car.position, (trip.start_x, trip.start_y))
    good_time = go_distance + car.time <= trip.earliest
    trip.score = distance_trip + (bonus if good_time else 0)
    trip.car = car
    car.trips.append(trip)
    meters = count_m(car, trip)
    car.time += meters
    car.position = (trip.finish_x, trip.finish_y)
    waiting.append((car, meters))
    return trip


def write_in_file(path, cars):
    score = 0
    with open(path, 'w') as f:
        for car in cars:
            f.write('{} '.format(len(car.trips)))
            for trip in car.trips:
                f.write('{} '.format(trip.id))
                score += trip.score
            f.write('\n')
        f.write('Score: {}'.format(score))


if __name__ == '__main__':
    pathes = [
        "/Users/zlatahayvoronska/Documents/Algorithms/Ad fontes/Self_driving_cars/qualification_round_2018/a_example.in"]
        # "/Users/zlatahayvoronska/Documents/Algorithms/Ad fontes/Self_driving_cars/qualification_round_2018/b_should_be_easy.in",
        # "/Users/zlatahayvoronska/Documents/Algorithms/Ad fontes/Self_driving_cars/qualification_round_2018/c_no_hurry.in",
        # "/Users/zlatahayvoronska/Documents/Algorithms/Ad fontes/Self_driving_cars/qualification_round_2018/d_metropolis.in",
        # "/Users/zlatahayvoronska/Documents/Algorithms/Ad fontes/Self_driving_cars/qualification_round_2018/e_high_bonus.in"]
    a = 0
    for k in range(1, 4):
        print("Variant:", k)
        for i in range(len(pathes)):
            print("Path:", i)
            data = reading(pathes[i])
            trips, rows, cols, n_vehicles, bonus, time = reading_2(data)
            cars = [Car(i + 1) for i in range(n_vehicles)]
            waiting = []
            for car in cars:
                characterize_car(car, trips, time, bonus, waiting, k)

            while len(waiting) > 0:
                waiting = sorted(waiting, key=lambda x: x[1])

                car, wait_time = waiting[0]
                waiting.pop(0)
                characterize_car(car, trips, time, bonus, waiting, k)

            r = 'example' + str(a) + '.txt'
            a += 1
            write_in_file(r, cars)
