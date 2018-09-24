
import Generators
import Clustering
import Linkers
import Metrics

def main():
	graph_creator = Linkers.MultiradiusLinkFinder([(20, 15), (5, 100)], Metrics.L2_distance)
	clusterer = Clustering.MapClusterer(Generators.WhiteNoiseGenerator(3000,500).points, graph_creator)
	r = clusterer.run_search(sensitivity=12)
	print("Found solution with sensitivity: {1} and pr_alpha: {2} result length: {0}".format(len(r), 12, 0.95))
	open("result.txt", 'w').write(str(r))
	return r

if __name__ == "__main__":
	main()
	exit(0)
