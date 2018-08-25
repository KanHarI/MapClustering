
import Generators
import Clustering

def main():
	r = len(Clustering.clustering(Generators.JsonGenerator("locations.json").points, 20))
	print("Solution size: " + str(r))
	return 0

if __name__ == "__main__":
	main()
