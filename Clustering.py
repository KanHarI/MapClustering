
import math
import copy
import numpy as np
import networkx as nx
import progressbar


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


class DefaultLinkFinder:
	def __init__(self, max_distance=None, num_neighbors=10, distance_func=L2_distance):
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

	def calculate_point_distances(self):
		point_distances = []
		for center_pt in progressbar.progressbar(range(self.size)):
			point_distances.append(
				np.array(list(map(
					lambda i: point_distances[i][center_pt] if (i < center_pt) else
					self.distance_func(self.points[i], self.points[center_pt]),
					range(self.size)
					)))
				)
		self.point_distances = np.array(point_distances)


	def find_links(self):
		self.links = []
		for center_pt in progressbar.progressbar(range(self.size)):
			self.links.append(self.find_neighbors(center_pt))
		self.links=np.array(self.links)
	
	def find_neighbors(self, center_pt):
		possible_neighbors = []
		for dst in range(self.size):
			if self.max_distance is not None and self.point_distances[center_pt][dst] > self.max_distance:
				continue
			possible_neighbors.append(dst)
		possible_neighbors.sort(key=lambda i: self.point_distances[center_pt][i])
		if self.num_neighbors:
			possible_neighbors = possible_neighbors[:self.num_neighbors]
		return np.array(possible_neighbors)

	def create_graph(self):
		self.graph = nx.DiGraph()
		for pi in range(self.size):
			self.graph.add_node(pi)
		for pi in range(self.size):
			for di in self.links[pi]:
				self.graph.add_edge(pi,di)


class MultiradiusLinkFinder(DefaultLinkFinder):
	def __init__(self, distance_neighbor_list, distance_func=L2_distance):
		super().__init__(0,0,distance_func)
		# A list of distance-number of neighbors pairs, ordered
		# from smallest radius and most neighbors to greatest radius
		# and least neighbors
		self.distance_neighbor_list = distance_neighbor_list

	def find_neighbors(self, center_pt):
		max_distance = self.distance_neighbor_list[-1][0]
		possible_neighbors = []
		for dst in range(self.size):
			if max_distance is not None and self.point_distances[center_pt][dst] > max_distance:
				continue
			possible_neighbors.append(dst)
		possible_neighbors.sort(key=lambda i: self.point_distances[center_pt][i])

		distance_neighbor_list_ptr = 0
		i = 0
		while i < len(possible_neighbors):
			if i > self.distance_neighbor_list[distance_neighbor_list_ptr][1]:
				possible_neighbors = possible_neighbors[:i]
				break
			if self.point_distances[center_pt][i] > distance_neighbor_list[distance_neighbor_list_ptr][0]:
				distance_neighbor_list_ptr += 1
				if distance_neighbor_list_ptr >= len(distance_neighbor_list):
					possible_neighbors = possible_neighbors[:i]
					break
			i += 1


		return np.array(possible_neighbors)


class MapClusterer:
	def __init__(self, points, graph_creator):
		print("Initializing MapClusterer object:")
		self.points = points
		self.size = len(self.points)
		self.graph = graph_creator.run(self.points)


	def run_search(self, sensitivity=7, pr_alpha=0.95):
		print("Running search...")
		solution = []
		graph = copy.deepcopy(self.graph)
		pb = progressbar.ProgressBar(max_value=self.size)

		while(graph.number_of_nodes() > 0):
			pb.update(self.size - graph.number_of_nodes())
			p_rank = nx.pagerank(graph, alpha=pr_alpha)
			maximally_ranked_node = max(p_rank, key=lambda i: p_rank[i])
			max_rank = p_rank[maximally_ranked_node]

			# Priritizing low-connectivity nodes in the network
			modified_p_rank = {key: (math.exp((max_rank - value)*sensitivity/max_rank)) for (key, value) in p_rank.items()}
			
			# my_rank takes into account all neighbors of a possible nodes.
			# The iteration is over self.graph.nodes() and not over 
			# graph.nodes() as sometimes a node already removed from the graph
			# will be the best match.
			my_rank = {}
			for node in self.graph.nodes():
				rank = 0
				for neighbor in self.graph.successors(node):
					if neighbor not in graph.nodes():
						continue
					rank += modified_p_rank[neighbor]
				my_rank[node] = rank
			maximally_ranked_node = max(p_rank, key=lambda i: my_rank[i])
			solution.append((maximally_ranked_node, list(graph.successors(maximally_ranked_node))))
			graph.remove_nodes_from(graph.successors(maximally_ranked_node))
		pb.finish()
		return solution
