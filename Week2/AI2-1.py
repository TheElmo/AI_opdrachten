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
@lru_cache(maxsize=None)
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
            travel_distance = distance(city,neighbor)
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
    route = find_crossings(nn_result)
    for x in range(10000):
        print("gone through", x , "times")
        route = find_crossings(route)
    return route

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
    visited_combinations = []
    for i in (range(int(len(route)))):
        for a in (range(int(len(route)))):
            if i == a:
                continue
            comb_key = str(i) + str(a)
            comb_key = "".join(sorted(comb_key))
            if comb_key in visited_combinations:
                continue
            visited_combinations.append(comb_key)
            data = get_connection(route,i)
            data2 = get_connection(route,a)
            connection1 = data[1]
            key1 = data[0]
            connection2 = data2[1]
            key2 = data2[0]

            index1 = data[2]
            index2 = data[3]
            index3 = data2[2]
            index4 = data2[3]

            segment1 = get_xy_values(key1)
            segment2 = get_xy_values(key2)
            if does_cross(segment1,segment2):
                # print(segment1, ' and ', segment2, " cross")
                # print(index1,index2,index3,index4)
                new_route = route.copy()
                #NOT SURE HOW TO FLIP, WITHOUT +1 it doesn't work?
                old_distance = distance(route[min(index1,index2)],route[max(index1,index2)]) + distance(route[min(index3,index4)],route[max(index3,index4)])
                new_route[index2:index3+1] = reversed(route[index2:index3+1])
                new_distance = distance(new_route[min(index1,index2)],new_route[max(index1,index2)]) + distance(new_route[min(index3,index4)],new_route[max(index3,index4)])
                if new_distance < old_distance:
                    route = new_route.copy()
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
    return [key,connection,index,next_index]

def get_xy_values(key):
    city1 = key.split("|")[0]
    city2 = key.split("|")[1]
    x_value1 = int(city1.split(":")[0])
    y_value1 = int(city1.split(":")[1])
    x_value2 = int(city2.split(":")[0])
    y_value2 = int(city2.split(":")[1])
    return [x_value1,y_value1,x_value2,y_value2]

def does_cross(segment1,segment2):
    #Naar https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    x1 = segment1[0]
    x2 = segment1[2]
    x3 = segment2[0]
    x4 = segment2[2]

    y1 = segment1[1]
    y2 = segment1[3]
    y3 = segment2[1]
    y4 = segment2[3]

    if (max(x1,x2) < min(x3,x4)):
        return False #There are no shared x coordinates
    try:
        a1 = (y1-y2)/(x1-x2)
        a2 = (y3-y4)/(x3-x4)
    except ZeroDivisionError:
        return False
    b1 = y1-a1*x1 #= y2-a1*x2
    b2 = y3-a2*x3 #= y4-a2*x4

    if a1 == a2:
        return False #Lines are parralel and will never cross

    try:
        Xa = round((b2-b1) / (a1-a2))
    except ZeroDivisionError:
        return False
    if Xa in segment1 or Xa in segment2:
        return False #Crossing exists but is multual city
    if Xa < max( min(x1,x2), min(x3,x4) ) or Xa > min( max(x1,x2), max(x3,x4) ):
        return False
    else:
        return True

@lru_cache(maxsize=None)
def linear_function(a,x,b):
    return (a*x) +b

@lru_cache(maxsize=None)
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
            con_distance = distance(previous_city,city)
            total_distance += con_distance
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
#plot_tsp(nearest_neighbor,make_cities(500))

#B
# Total distance for 500 cities: 797860

#D
plot_tsp(nearest_neighbor_2opt,make_cities(500))