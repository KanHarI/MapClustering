
import Generators
import Clustering

def main():
	graph_creator = Clustering.MultiradiusLinkFinder([(20, 15), (5, 100)], Clustering.L2_distance)
	clusterer = Clustering.MapClusterer(Generators.WhiteNoiseGenerator(3000,1000).points, graph_creator)
	r = clusterer.run_search(sensitivity=12)
	print("Found solution with sensitivity: {1} and pr_alpha: {2} result length: {0}".format(len(r), 12, 0.95))
	open("result.txt", 'w').write(str(r))
	return 0

if __name__ == "__main__":
	main()
