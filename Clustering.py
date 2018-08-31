
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


def take_while(generator, cond):
	for g in generator:
		if not cond(g):
			raise StopIteration
		yield g


class MapClusterer:
	def __init__(self, points, num_neighbors, distance_func = L2_distance, max_distance=None):
		print("Initializing MapClusterer object:")
		self.points = points
		self.size = len(self.points)
		self.num_neighbors = num_neighbors
		self.max_distance = max_distance
		self.distance_func = distance_func
		print("Calculating point distances...")
		self.calculate_point_distances()
		print("Finding links...")
		self.find_links()
		print("Creating graph...")
		self.create_graph()

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
		self.links = np.array(
			list(
				map(
					lambda center_pt: np.array(list(take_while(
						sorted(
							range(self.size),
							key=lambda i: self.point_distances[center_pt][i]
							),
						lambda i: (self.max_distance is None) or (self.point_distances[center_pt][i] < self.max_distance)))[:self.num_neighbors]),
					range(self.size))))


	def create_graph(self):
		self.graph = nx.DiGraph()
		for pi in range(self.size):
			self.graph.add_node(pi)
		for pi in range(self.size):
			for di in self.links[pi]:
				self.graph.add_edge(pi,di)


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
			
			# My rank takes into account all neighbors of a possible nodes.
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
