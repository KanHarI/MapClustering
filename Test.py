
import Generators
import Clustering

def main():
	r = Clustering.MapClusterer(Generators.WhiteNoiseGenerator(1000).points, 10, Clustering.L2_distance, 0.05).run_search()
	print("Found solution! result length: {0}".format(len(r)))
	return 0

if __name__ == "__main__":
	main()
