
import networkx as nx
import copy

class PartialPageRank:
	def __init__(self, graph, alpha, init_iterations=20):
		# ppr stands for PartialPageRank
		self.graph = graph
		self.alpha = alpha
		self.weights = {}
		default_weight = 1. / self.graph.number_of_nodes()
		for node in self.graph.nodes():
			self.weights[node] = default_weight
		self.iterate_alg(init_iterations)

	def iterate_alg(self, repeats):
		default_weight = 1. / self.graph.number_of_nodes()
		self.dangling_nodes=[]
		for node in self.graph.nodes():
			if self.graph.out_degree(node) == 0:
				self.dangling_nodes.append(node)
		for i in range(repeats):
			wlast = copy.copy(self.weights)
			for node in self.weights.keys():
				self.weights[node] = 0
			danglesum = self.alpha * sum(wlast[node] for node in self.dangling_nodes)
			for node in self.graph:
				od = self.graph.out_degree(node)
				for neighbor in self.graph[node]:
					self.weights[neighbor] += self.alpha*wlast[node]/od
				self.weights[node] += (1 - self.alpha)*default_weight
				self.weights[node] += self.alpha*danglesum*default_weight
			self.err = sum(abs(self.weights[node] - wlast[node]) for node in self.graph.nodes())

	def remove_nodes(self, rem_nodes, iterations=2):
		rem_nodes = list(rem_nodes)
		removed_sum = sum(self.weights[node] for node in rem_nodes)
		for node in rem_nodes:
			self.weights.pop(node)
		self.graph.remove_nodes_from(rem_nodes)
		remaining_nodes = self.graph.number_of_nodes()
		if remaining_nodes == 0:
			return
		mult = 1. / (1 - removed_sum)
		for node in self.graph.nodes():
			self.weights[node] *= mult
		self.iterate_alg(iterations)
