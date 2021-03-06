
import Generators
import Clustering
import Linkers
import Metrics

def main():
	graph_creator = Linkers.DefaultLinkFinder(max_distance=0.03, num_neighbors=10, distance_func=Metrics.L2_distance)
	# Distance is cropped to 25 miles to allow more efficient computation

	clusterer = Clustering.MapClusterer(Generators.WhiteNoiseGenerator(2000).points, graph_creator)
	r = clusterer.run_search(sensitivity=7, pr_alpha=0.95, pr_accuracy=1)
	print("Found solution with sensitivity: {1} pr_alpha: {2} pr_accuracy: {3} result length: {0}".format(len(r), 7, 0.95, 1))
	open("result.txt", 'w').write(str(r))
	return r

if __name__ == "__main__":
	main()
	exit(0)
