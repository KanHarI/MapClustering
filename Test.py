
import Generators
import Clustering

def main():
	r = len(Clustering.clustering(Generators.WhiteNoiseGenerator(2000).points, 20))
	print("Solution size: " + str(r))
	return 0

if __name__ == "__main__":
	main()
