
import math

# Defining distance functions for different metric spaces
def L2_distance(p1, p2):
	dx = p1[0]-p2[0]
	dy = p1[1]-p2[1]
	return math.sqrt(dx**2+dy**2)

def taxicab_distance(p1, p2):
	dx = p1[0]-p2[0]
	dy = p1[1]-p2[1]
	return abs(dx)+abs(dy)

def geographic_distance(p1, p2):
	import geopy.distance
	return geopy.distance.vincenty(p1, p2).miles
