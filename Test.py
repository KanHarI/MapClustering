
import Generators
import Clustering

def main():
	min_size = 1000
	for i in range(1000):
		r = Clustering.clustering(Generators.JsonGenerator("locations.json").points, 20)
		if (len(r) < min_size):
			min_size = len(r)
			print(r)
			print("Best solution size: " + str(len(r)))
	return 0

if __name__ == "__main__":
	main()
