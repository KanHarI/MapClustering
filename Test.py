
import Generators
import Clustering

def main():
	graph_creator = Clustering.MultiradiusLinkFinder([(25, 1000), (50,10)], Clustering.geographic_distance)
	clusterer = Clustering.MapClusterer(Generators.JsonGenerator("stores.json").points, graph_creator)
	r = clusterer.run_search(sensitivity=12)
	print("Found solution with sensitivity: {1} and pr_alpha: {2} result length: {0}".format(len(r), 12, 0.95))
	open("result.txt", 'w').write(str(r))
	return 0

if __name__ == "__main__":
	main()
