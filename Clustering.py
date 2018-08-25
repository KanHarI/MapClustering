
import scipy.spatial
import math
import copy

def clustering(points, num_neighbors):
	assert len(points) > num_neighbors
	print("Creating local maps...")
	local_maps = {i:generate_local_map_from_point(i,points,num_neighbors) for i in range(len(points))}
	print("Running search:")
	index_translation = {i:i for i in range(len(points))}
	uncovered_indices = list(range(len(points)))
	uncovered_points = copy.deepcopy(points)
	fit_pts = []

	while len(uncovered_indices) > 0:
		if len(uncovered_indices) < 3:
			hull = uncovered_indices
		else:
			hull = list(map(lambda x: index_translation[x], scipy.spatial.ConvexHull(uncovered_points).vertices))

		points_with_hull_in_local_map = []
		for i in uncovered_indices:
			if any(map(lambda ph: ph in local_maps[i], hull)):
				points_with_hull_in_local_map.append(i)

		fit_pt = max(points_with_hull_in_local_map, key = lambda p: pt_fitness(p, uncovered_indices, local_maps, hull))
		radius = max(
			map(lambda p: L2_distance(points[fit_pt], points[p]), local_maps[fit_pt])
			)
		# radius is in distance of lat&long...
		fit_pts.append({"pt": fit_pt, "neighbors": local_maps[fit_pt], "radius": radius})

		for i in local_maps[fit_pt]:
			if i in uncovered_indices:
				uncovered_indices.remove(i)
				uncovered_points.remove(points[i])

		index_translation = {i:uncovered_indices[i] for i in range(len(uncovered_indices))}

	return fit_pts


# Trying to minimize "Surface tension"
# Should probably add more paramters and improve this function
# maybe try to find distance of local mapped points from center of mass?
def pt_fitness(pt, uncovered_indices, local_maps, hull):
	fitness = 0
	for i in local_maps[pt]:
		if i in uncovered_indices:
			fitness += 1
		if i in hull:
			fitness += 100
	return fitness


def L2_distance(p1, p2):
	dx = p1[0]-p2[0]
	dy = p1[1]-p2[1]
	return math.sqrt(dx**2+dy**2)


def generate_local_map_from_point(pt_index, points, num_neighbors):
	center_pt = points[pt_index]
	sorted_pts = sorted(range(len(points)), key = lambda i: L2_distance(points[i], center_pt))
	return sorted_pts[:num_neighbors]
