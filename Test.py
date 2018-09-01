
import Generators
import Clustering

def main():
	graph_creator = Clustering.MultiradiusLinkFinder([(30, 0.07), (15, 0.1)], Clustering.L2_distance)
	clusterer = Clustering.MapClusterer(Generators.WhiteNoiseGenerator(2000).points, graph_creator)
	r = clusterer.run_search(sensitivity=12)
	print("Found solution with sensitivity: {1} and pr_alpha: {2} result length: {0}".format(len(r), 12, 0.95))
	open("result.txt", 'w').write(str(r))
	return 0

if __name__ == "__main__":
	main()
