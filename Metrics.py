
import math
import geopy.distance

# Defining distance functions for different metric spaces
def L2_distance(p1, p2):
	dx = p1[0]-p2[0]
	dy = p1[1]-p2[1]
	return math.sqrt(dx**2+dy**2)

def taxicab_distance(p1, p2):
	dx = p1[0]-p2[0]
	dy = p1[1]-p2[1]
	return abs(dx)+abs(dy)

def geographic_distance(p1, p2):
	return geopy.distance.vincenty(p1, p2).miles


EARTH_RADIUS_IN_MILES = 3959.0

class CroppedGeographicDistance:
	def __init__(self, crop_distance):
		self.calc_error = 0.2 # approximated. should be high enough (way already high enough at 0.1, raised for security)
		self.crop_distance = float(crop_distance)
		self.most_polar = 0
		self.max_long_delta = 360 # whole circle is allowed until callibration into polar points
		self.max_lat_delta = math.asin(crop_distance / EARTH_RADIUS_IN_MILES) * 180/math.pi
		self.max_lat_delta *= 1 + self.calc_error

	def __call__(self, p1, p2):
		if max(abs(p1[0]), abs(p2[0])) > self.most_polar:
			self.most_polar = max(abs(p1[0]), abs(p2[0]))
			if self.most_polar > 80:
				print("Warning: exteremely polar points in dataset. should modify algorithm for optimal results")
			self.max_long_delta = math.asin(self.crop_distance / EARTH_RADIUS_IN_MILES) / math.cos(self.most_polar * math.pi/180) * 180/math.pi
			self.max_long_delta *= 1 + self.calc_error

		if abs(p1[0]-p2[0]) > self.max_lat_delta or abs(p1[1]-p2[1]) > self.max_long_delta:
			return self.crop_distance*2 # fake result that is high enough so we don't care

		return geopy.distance.vincenty(p1, p2).miles
