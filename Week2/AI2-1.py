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

def nearest_neighbor_2opt(cities):
    nn_result = nearest_neighbor(cities)
    find_linear_functions(cities)
    return find_crossings(nn_result)

def find_linear_functions(cities):
    for city in cities:
        for other_city in cities:
            if city == other_city:
                continue
            line = get_linear(city[0],city[1],other_city[0],other_city[1])
            key = create_key(city[0],city[1],other_city[0],other_city[1])
            mirror_key = create_key(other_city[0],other_city[1],city[0],city[1])
            if mirror_key not in connections:
                connections[key] = line

def find_crossings(route):
    for i in (range(int(len(route)))):
        for a in (range(int(len(route)))):
            print("I:",i,"A:",a)

            if i == a:
                continue
            data = get_connection(route,i)
            data2 = get_connection(route,a)
            connection1 = data[1]
            key1 = data[0]
            index1 = data[2]
            index2 = data[3]
            index3 = data2[2]
            index4 = data2[3]
            connection2 = data2[1]
            key2 = data2[0]
            crossings = check_y(key1,connection1,connection2, index1,index2,index3,index4)
            for crossing in crossings:
                city_index1 = crossings[crossing][0]
                city_index2 = crossings[crossing][1]
                city_index3 = crossings[crossing][2]
                city_index4 = crossings[crossing][3]

                print(crossings[crossing])
    return route

def get_connection(route,index):
    next_index = index+1
    if next_index > len(route)-1:
        next_index = 0
    next_city = route[next_index]
    city = route[index]
    # print(city,next_city)
    x1,y1 = city[0], city[1]
    x2,y2 = next_city[0], next_city[1]
    connection = None
    try:
        key = create_key(x1,y1,x2,y2)
        connection = connections[key]
    except KeyError:
        try:
            key = create_key(x2,y2,x1,y1)
            connection = connections[key]
        except KeyError:
            print("Help")
            pass
    return [key,connection,index,index+1]

def get_coordinates(key,connection):
    city1 = key.split("|")[0]
    city2 = key.split("|")[1]
    x_value1 = float(city1.split(":")[0])
    y_value1 = float(city1.split(":")[1])
    x_value2 = float(city2.split(":")[0])
    y_value2 = float(city2.split(":")[1])
    return [[x_value1,x_value2],[y_value1,y_value2]]

def check_y(key1,connection1,connection2,index1,index2,index3,index4):
    crossings = {}
    xy_values = get_coordinates(key1,connection1)
    #print(xy_values)
    x_values = xy_values[0]
    y_values = xy_values[1]
    if x_values[0] < x_values[1]:
        low_x = x_values[0]
        high_x = x_values[1]
    else:
        low_x = x_values[1]
        high_x = x_values[0]

    if y_values[0] < y_values[1]:
        low_y = y_values[0]
        high_y = y_values[1]
    else:
        low_y = y_values[1]
        high_y = y_values[0]
    print(low_x,high_x,low_y,high_y)
    #FIX X bound
    for x in range(int(low_x)+1, int(high_x)):
        #print("Findin y for x:", x)
        y1 = int(linear_function(connection1[0],x,connection1[1]))
        y2 = int(linear_function(connection2[0],x,connection2[1]))
        # print(y1,y2)
        # print(low_y,high_y)
        lowest_y = None
        highest_y = None
        if y1 > y2:
            lowest_y = y1
            highest_y = y2
        else:
            lowest_y = y2
            highest_y = y2

        if lowest_y < low_y:
            continue
        if highest_y >= high_y:
            break
        if y1 == y2:
            crossings[y1] = [index1,index2,index3,index4]
            print("HERE")
            print(y1,y2)
    # print("---")
    return crossings

@lru_cache(maxsize=None)
def linear_function(a,x,b):
    return (a*x) +b

def get_linear(x1,y1,x2,y2):
    points = [(x1,y1),(x2,y2)]
    x_coords, y_coords = zip(*points)
    val = vstack([x_coords,ones(len(x_coords))]).T
    a, b = lstsq(val, y_coords,rcond=None)[0]
    a = float(a)
    b = float(b)
    return [a,b]

def create_key(x1,y1,x2,y2):
    return "{0:d}:{1:d}|{2:d}:{3:d}".format(x1,y1,x2,y2)

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

    random.seed(1) # the current system time is used as a seed
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