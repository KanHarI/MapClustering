
import scipy.spatial
import math
import copy
import random
import numpy

def L2_distance(p1, p2):
	dx = p1[0]-p2[0]
	dy = p1[1]-p2[1]
	return math.sqrt(dx**2+dy**2)


def taxicab_distance(p1, p2):
	dx = p1[0]-p2[0]
	dy = p1[1]-p2[1]
	return abs(dx)+abs(dy)


distance_normalizer = []


def clustering(points, num_neighbors, randomness=0.5, distance_func = L2_distance):
	global distance_normalizer
	assert len(points) > num_neighbors
	
	distance_normalizer = []
	local_maps = {i:generate_local_map_from_point(i,points,num_neighbors,distance_func) for i in range(len(points))}
	
	distance_normalizer = numpy.mean(distance_normalizer)

	index_translation = {i:i for i in range(len(points))}
	uncovered_indices = list(range(len(points)))
	uncovered_points = copy.deepcopy(points)
	fit_pts = []

	while len(uncovered_indices) > 0:
		if len(uncovered_indices) < 3:
			hull = uncovered_indices
		else:
			hull = list(map(lambda x: index_translation[x], scipy.spatial.ConvexHull(uncovered_points).vertices))

		hull_angles = {}
		for i in range(len(hull)):
			h_prev = points[hull[(i-1) % len(hull)]]
			h_cur = points[hull[i]]
			h_next = points[hull[(i+1) % len(hull)]]

			l1 = (h_cur[0] - h_prev[0], h_cur[1] - h_prev[1])
			l2 = (h_next[0] - h_cur[0], h_next[1] - h_cur[1])

			tmp = abs(math.atan2(*l1)-math.atan2(*l2))
			hull_angles[hull[i]] = min(tmp, 2*math.pi-tmp)

		com = find_center_of_mass(uncovered_points)

		points_with_hull_in_local_map = []
		for i in uncovered_indices:
			if any(map(lambda ph: ph in local_maps[i], hull)):
				points_with_hull_in_local_map.append(i)

		sorted_pts = sorted(points_with_hull_in_local_map, key = lambda p: -pt_fitness(p, uncovered_indices, local_maps, hull, hull_angles, com, points, distance_func))
		fit_pt = 0
		while fit_pt < len(sorted_pts) - 1:
			if random.random() > randomness:
				break
			fit_pt += 1
		fit_pt = sorted_pts[fit_pt]

		radius = max(map(lambda p: distance_func(points[fit_pt], points[p]), local_maps[fit_pt]))
		# radius is in distance of lat&long...
		fit_pts.append({"pt": fit_pt, "neighbors": local_maps[fit_pt], "radius": radius})

		for i in local_maps[fit_pt]:
			if i in uncovered_indices:
				uncovered_indices.remove(i)
				uncovered_points.remove(points[i])

		index_translation = {i:uncovered_indices[i] for i in range(len(uncovered_indices))}

	return fit_pts

def find_center_of_mass(pts):
	xsum = sum(map(lambda x: x[0], pts))
	ysum = sum(map(lambda x: x[1], pts))
	return (xsum/len(pts), ysum/len(pts))

# Trying to minimize "Surface tension"
# Should probably add more paramters and improve this function
# maybe try to find distance of local mapped points from center of mass?
def pt_fitness(pt, uncovered_indices, local_maps, hull, hull_angles, com, points, distance_func):
	fitness = 0
	for i in local_maps[pt]:
		if i in uncovered_indices:
			fitness += distance_func(points[i], com)/distance_normalizer*2.04
		if i in hull:
			fitness += 20*hull_angles[i]
	return fitness

def generate_local_map_from_point(pt_index, points, num_neighbors, distance_func):
	center_pt = points[pt_index]
	
	# Allows for distance normalization
	global distance_normalizer
	distance_normalizer.append(numpy.mean(list(map(lambda i: distance_func(points[i], center_pt), range(len(points))))))

	sorted_pts = sorted(range(len(points)), key = lambda i: distance_func(points[i], center_pt))
	return sorted_pts[:num_neighbors]
