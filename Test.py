
import Generators
import Clustering
import Linkers
import Metrics

def main():
	graph_creator = Linkers.MultiradiusLinkFinder([(20, 15), (5, 100)], Metrics.L2_distance)
	clusterer = Clustering.MapClusterer(Generators.WhiteNoiseGenerator(3000,500).points, graph_creator)
	r = clusterer.run_search(sensitivity=7, pr_alpha=0.95, pr_accuracy=1)
	print("Found solution with sensitivity: {1} pr_alpha: {2} pr_accuracy: {3} result length: {0}".format(len(r), 7, 0.95, 1))
	open("result.txt", 'w').write(str(r))
	return r

if __name__ == "__main__":
	main()
	exit(0)
