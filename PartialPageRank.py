
import copy

class PartialPageRank:
	def __init__(self, graph, alpha, init_iterations=20):
		self.graph = graph
		self.alpha = alpha
		self.weights = {}
		default_weight = 1. / self.graph.number_of_nodes()
		for node in self.graph.nodes():
			# initialize all weights to default
			self.weights[node] = default_weight
		self.iterate_alg(init_iterations)

	def iterate_alg(self, repeats):
		default_weight = 1. / self.graph.number_of_nodes()
		
		# Find nodes without successors,
		# effectively connecting them to all nodes in the graph
		self.dangling_nodes=[]
		for node in self.graph.nodes():
			# out_degree is number of successors. Math jargon.
			if self.graph.out_degree(node) == 0:
				self.dangling_nodes.append(node)

		# Iterate weights update for required number of iterations
		for i in range(repeats):
			# Copy weights, and finds the new weights after an iteration of
			# the algorithm
			wlast = copy.copy(self.weights)
			for node in self.weights.keys():
				self.weights[node] = 0
			# Find the sum of weights of all dangling nodes
			danglesum = self.alpha * sum(wlast[node] for node in self.dangling_nodes)
			# Update weight of neighbors based on a specific node
			for node in self.graph:
				od = self.graph.out_degree(node)
				for neighbor in self.graph.successors(node):
					# Propagate from currect node to all neighbors
					self.weights[neighbor] += self.alpha*wlast[node]/od
				# Update weight of current node from default (based on the dampening factor, alpha)
				self.weights[node] += (1 - self.alpha)*default_weight
				# Update weight of current node sapping weight from dangling nodes
				self.weights[node] += self.alpha*danglesum*default_weight
			self.err = sum(abs(self.weights[node] - wlast[node]) for node in self.graph.nodes())

	# Removes nodes AND updates pagerank result
	def remove_nodes(self, rem_nodes, iterations=2):
		rem_nodes = list(rem_nodes)
		removed_sum = sum(self.weights[node] for node in rem_nodes)
		for node in rem_nodes:
			self.weights.pop(node)
		self.graph.remove_nodes_from(rem_nodes)
		remaining_nodes = self.graph.number_of_nodes()
		if remaining_nodes == 0:
			return
		# Magnify all remaining weights such that the sum of them is one
		mult = 1. / (1 - removed_sum)
		for node in self.graph.nodes():
			self.weights[node] *= mult
		self.iterate_alg(iterations)
