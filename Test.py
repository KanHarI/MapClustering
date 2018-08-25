
import Generators
import Clustering

def main():
	r = Clustering.clustering(Generators.JsonGenerator("locations.json").points, 20)
	print(r)
	print("Solution size: " + str(len(r)))
	return 0

if __name__ == "__main__":
	main()
