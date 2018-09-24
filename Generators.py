
import random
import json

class WhiteNoiseGenerator:
	def __init__(self, n, r=1):
		self.points = []
		for i in range(n):
			self.points.append((random.random()*r,random.random()*r))

class JsonGenerator:
	def __init__(self, json_path):
		self.points = []
		c = json.loads(open(json_path, 'rb').read())
		for row in c:
			self.points.append((float(row['lat']), float(row['lng'])))
