
import math
import copy
import progressbar
import PartialPageRank as ppr

# The implimentation of the algorithm
class MapClusterer:
	# graph creator is the object responsible for finding the links between
	# the different nodes
	def __init__(self, points, graph_creator):
		print("Initializing MapClusterer object:")
		self.points = points
		self.size = len(self.points)
		self.graph = graph_creator.run(self.points)


	def add_details(self, solution):
		return list(map(lambda s: {
			"point": self.points[s[0]],
			"id": s[0],
			"label": self.graph.node[s[0]],
			"neighbors": s[1],
			"neighbors_points": list(map(lambda i: self.points[i], s[1])),
			"wasted_neighbors": s[2],
			"wasted_neighbors_points": list(map(lambda i: self.points[i], s[2]))
			}, solution))


	def run_search(self, sensitivity=7, pr_alpha=0.95):
		solution = []
		# Initialize the partial page rank object
		ppr_graph = ppr.PartialPageRank(copy.deepcopy(self.graph), alpha=pr_alpha)
		print("Running search...")
		pb = progressbar.ProgressBar(maxval=self.size)
		pb.start()
		while(ppr_graph.graph.number_of_nodes() > 0):
			# Find the current page rank result
			p_rank = ppr_graph.weights
			maximally_ranked_node = max(p_rank, key=lambda i: p_rank[i])
			max_rank = p_rank[maximally_ranked_node]

			# modified_p_rank is a rank that ranks isolated nodes exponentialy 
			# higher than well connected nodes
			modified_p_rank = {key: (math.exp((max_rank - value)*sensitivity/max_rank)) for (key, value) in p_rank.items()}
			
			# my_rank ranks a node higher proportionaly to the amount of
			# isolated nodes it touches
			my_rank = {}
			for node in ppr_graph.graph.nodes():
				rank = 0
				for neighbor in self.graph.successors(node):
					if neighbor not in ppr_graph.graph.nodes():
						continue
					rank += modified_p_rank[neighbor]
				my_rank[node] = rank

			# Find highest ranked node of current graph
			maximally_ranked_node = max(p_rank, key=lambda i: my_rank[i])

			# Neighbors of selected node that where already covered by the solution
			wasted_points = list(filter(lambda x: x not in ppr_graph.graph.nodes, self.graph.successors(maximally_ranked_node)))
			
			solution.append((maximally_ranked_node, list(ppr_graph.graph.successors(maximally_ranked_node)), wasted_points))
			
			# removes nodes and also updates page rank rankings
			ppr_graph.remove_nodes(ppr_graph.graph.successors(maximally_ranked_node))
			
			pb.update(self.size - ppr_graph.graph.number_of_nodes())

		pb.finish()
		return self.add_details(solution)
