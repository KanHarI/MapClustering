
import Generators
import Clustering

def main():
	clusterer = Clustering.MapClusterer(Generators.WhiteNoiseGenerator(1000).points, 10, Clustering.L2_distance, 0.05)
	r = clusterer.run_search(sensitivity=12)
	print("Found solution with sensitivity: {1} and pr_alpha: {2} result length: {0}".format(len(r), 12, 0.95))
	open("result.txt", 'w').write(str(r))
	return 0

if __name__ == "__main__":
	main()
