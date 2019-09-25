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

#Connects the cities by choosing the nearest city that hasn't been visited yet
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

#Uses nearest neighbor but afterwards does 10.000 iterations of 2_opt to try and remove crossings
def nearest_neighbor_2opt(cities):
    nn_result = nearest_neighbor(cities)
    route = find_crossings(nn_result)
    for x in range(10):
        print("gone through", x , "times")
        route = find_crossings(route)
    return route

def nearest_neighbor_2opt_real(cities):
    nn_result = nearest_neighbor(cities)
    nn_result = nn_result + [nn_result[0]]
    route = nn_2opt(nn_result)
    return route

def nn_2opt(route):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route)-2):
           for j in range(i+1, len(route)):
                if j-i == 1: continue # changes nothing, skip then
                new_route = route[:]
                new_route[i:j] = route[j-1:i-1:-1] # this is the 2woptSwap
                if tour_length(new_route) < tour_length(best):
                     best = new_route
                     improved = True
        route = best
    return best


#Checks each road with all other roads in the route for crossings, 
#if a crossing is found it will destroy the 2 roads and create 2 new ones
#it wil apply this change if the distance of the 2 new roads is shorter then the 2 old ones
def find_crossings(route):
    visited_combinations = []
    for i in (range(len(route))):
        for a in (range(len(route))):
            if i == a:
                continue
            comb_key = (min(i,a),max(i,a))
            if comb_key in visited_combinations:
                continue
            visited_combinations.append(comb_key)
            next_i = i+1
            if next_i > len(route)-1:
                next_i = 0
            next_a = a+1
            if next_a > len(route)-1:
                next_a = 0
            index1 = i
            index2 = next_i
            index3 = a
            index4 = next_a
            segment1 = [route[i].x,route[i].y,route[next_i].x,route[next_i].y]
            segment2 = [route[a].x,route[a].y,route[next_a].x,route[next_a].y]
            if does_cross(segment1,segment2):
                new_route = route.copy()
                old_distance = distance(route[min(index1,index2)],route[max(index1,index2)]) + distance(route[min(index3,index4)],route[max(index3,index4)])
                new_route[index2:index3+1] = reversed(route[index2:index3+1])
                new_distance = distance(new_route[min(index1,index2)],new_route[max(index1,index2)]) + distance(new_route[min(index3,index4)],new_route[max(index3,index4)])
                if new_distance < old_distance:
                    route = new_route.copy()
    return route

#Returns True if 2 line segments cross
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
plot_tsp(nearest_neighbor_2opt,make_cities(20))

#plot_tsp(nearest_neighbor_2opt_real,make_cities(75))