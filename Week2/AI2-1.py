import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple
from copy import deepcopy
from functools import lru_cache
from numpy import ones,vstack
from numpy.linalg import lstsq

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('city', 'x y')
connections = {}
def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)

def nearest_neighbor(cities):
    visited_cities = []
    city = next(iter(cities))
    while len(visited_cities) != len(cities):
        visited_cities.append(city)
        small_distance = 0
        for neighbor in cities:
            if neighbor == city:
                continue
            if neighbor in visited_cities:
                continue
            travel_distance = calculate_travel_distance(city,neighbor)
            if small_distance == 0:
                city = neighbor
                small_distance = travel_distance
            elif travel_distance < small_distance:
                city = neighbor
                small_distance = travel_distance
    result = visited_cities
    return result
# line = get_linear(city_x_value,city_y_value,neighbor_x_value,neighbor_y_value)
#     key = create_key(city_x_value,city_y_value,neighbor_x_value,neighbor_y_value)
#     connections[key] = line
def nearest_neighbor_2opt(cities):
    nn_result = nearest_neighbor(cities)
    return find_crossings(nn_result)

def find_crossings(route):
    iterator = iter(route)
    city = next(iterator)
    previous_city = deepcopy(city)
    finished = False
    #print(connections.keys())
    #print(connections['29914137582'])
    while not finished:
        try:
            city = next(iterator)
            #print(previous_city)
            #print(city)
        except StopIteration:
            finished = True
        else:
            x1,y1 = previous_city[0], previous_city[1]
            x2,y2 = city[0], city[1]
            connection = None
            try:
                connection = connections[create_key(x1,y1,x2,y2)]
            except KeyError:
                pass
            print(previous_city, city)
            previous_city = deepcopy(city)
            print(connection)
    return route

@lru_cache(maxsize=None)
def linear_function(a,x,b):
    return a*x +b

def get_linear(x1,y1,x2,y2):
    points = [(x1,y1),(x2,y2)]
    x_coords, y_coords = zip(*points)
    val = vstack([x_coords,ones(len(x_coords))]).T
    a, b = lstsq(val, y_coords,rcond=None)[0]
    return [a,b]

def create_key(x1,y1,x2,y2):
    return "{0:d}{1:d}{2:d}{3:d}".format(x1,y1,x2,y2)

#Calculates the travel distance from a city to a neighbor
def calculate_travel_distance(city, neighbor):
    city_x_value = city[0]
    city_y_value = city[1]

    neighbor_x_value = neighbor[0]
    neighbor_y_value = neighbor[1]
    
    horizontal_distance = abs(city_x_value - neighbor_x_value)
    vertical_distance = abs(city_y_value - neighbor_y_value)
    travel_distance = horizontal_distance + vertical_distance
    return travel_distance

def cost(route):
    finished = False
    iterator = iter(route)
    city = next(iterator)
    previous_city = deepcopy(city)
    total_distance =0
    while not finished:
        try:
            city = next(iterator)
        except StopIteration:
            finished = True
        else:
            distance = calculate_travel_distance(previous_city,city)
            total_distance += distance
            previous_city = deepcopy(city)
    return total_distance

def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # cities is a set, sets don't support indexing
    start = next(iter(cities)) 
    return [[start] + list(rest)
            for rest in itertools.permutations(cities - {start})]

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) 
               for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed() # the current system time is used as a seed
    # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height))
                     for c in range(n))

def plot_tour(tour):
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.clock()
    tour = algorithm(cities)
    distance = cost(tour)
    print("Total distance", distance)
    t1 = time.clock()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)
    
#plot_tsp(try_all_tours, make_cities(10))
#A
#plot_tsp(nearest_neighbor,make_cities(10))

#B
# Total distance for 500 cities: 797860

#D
plot_tsp(nearest_neighbor_2opt,make_cities(10))