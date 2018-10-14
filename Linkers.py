
import progressbar
import numpy as np
import networkx as nx

import Metrics

# Finds num_neighbors closest points and makes them successors of every node
class DefaultLinkFinder:
	def __init__(self, max_distance=None, num_neighbors=10, distance_func=Metrics.L2_distance):
		self.distance_func = distance_func
		self.max_distance = max_distance
		self.num_neighbors = num_neighbors

	def run(self, points):
		self.size = len(points)
		self.points = points
		print("Calculating point distances...")
		self.calculate_point_distances()
		print("Finding links...")
		self.find_links()
		print("Creating graph...")
		self.create_graph()
		return self.graph

	# Calculate the distace between every 2 points in the set
	# Uses numpy array for efficiency
	def calculate_point_distances(self):
		point_distances = []
		pb = progressbar.ProgressBar(maxval=self.size)
		pb.start()
		for center_pt in range(self.size):
			point_distances.append(
				np.array(list(map(
					lambda i: point_distances[i][center_pt] if (i < center_pt) else
					self.distance_func(self.points[i], self.points[center_pt]),
					range(self.size)
					)))
				)
			pb.update(center_pt+1)
		pb.finish()
		self.point_distances = np.array(point_distances)


	def find_links(self):
		self.links = {}
		pb = progressbar.ProgressBar(maxval=self.size)
		pb.start()
		for center_pt in range(self.size):
			self.links[center_pt] = self.find_neighbors(center_pt)
			pb.update(center_pt+1)
		pb.finish()
	
	def find_neighbors(self, center_pt):
		possible_neighbors = []
		for dst in range(self.size):
			# Filters all points further away than max_distance
			if self.max_distance is not None and self.point_distances[center_pt][dst] > self.max_distance:
				continue
			possible_neighbors.append(dst)
		# Sort the possible neighboring points by descending distances
		# Take the num_neighbors closest points as neighbors
		if self.num_neighbors and self.num_neighbors < len(possible_neighbors):
			possible_neighbors.sort(key=lambda i: self.point_distances[center_pt][i])
			possible_neighbors = possible_neighbors[:self.num_neighbors]
		return possible_neighbors

	# Creates an nx graph from calculated properties
	def create_graph(self):
		self.graph = nx.DiGraph()
		for pi in range(self.size):
			self.add_node(pi)
		for pi in range(self.size):
			for di in self.links[pi]:
				self.graph.add_edge(pi,di)

	def add_node(self, n):
		self.graph.add_node(n)


# A specialized link finder, has multiple concentric rings of possible
# neighbors in different radi with different max_negihbors
# chooses the best fit for this point
class MultiradiusLinkFinder(DefaultLinkFinder):
	def __init__(self, distance_neighbor_list, distance_func=Metrics.L2_distance):
		super().__init__(0,0,distance_func)
		# A list of distance-number of neighbors pairs, ordered
		# from smallest radius and most neighbors to greatest radius
		# and least neighbors
		self.distance_neighbor_list = distance_neighbor_list
		self.node_labels = {}

	def add_node(self, n):
		self.graph.add_node(n, lbl=self.node_labels[n])


	# Overloads the DefaultLinkFinder's find_neighbors function
	def find_neighbors(self, center_pt):
		max_distance = self.distance_neighbor_list[-1][1]
		possible_neighbors = []
		for dst in range(self.size):
			if max_distance is not None and self.point_distances[center_pt][dst] > max_distance:
				continue
			possible_neighbors.append(dst)
		possible_neighbors.sort(key=lambda i: self.point_distances[center_pt][i])

		distance_neighbor_list_ptr = 0
		i = 0
		self.node_labels[center_pt] = distance_neighbor_list_ptr
		while i < len(possible_neighbors):
			if i >= self.distance_neighbor_list[distance_neighbor_list_ptr][0]:
				possible_neighbors = possible_neighbors[:i]
				break
			if self.point_distances[center_pt][possible_neighbors[i]] > self.distance_neighbor_list[distance_neighbor_list_ptr][1]:
				distance_neighbor_list_ptr += 1
				if distance_neighbor_list_ptr >= len(self.distance_neighbor_list):
					possible_neighbors = possible_neighbors[:i]
					break
				continue
			self.node_labels[center_pt] = distance_neighbor_list_ptr
			i += 1

		return np.array(possible_neighbors)
