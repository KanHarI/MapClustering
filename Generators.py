
import random
import json

class WhiteNoiseGenerator:
	def __init__(self, n):
		self.points = []
		for i in range(n):
			self.points.append((random.random(),random.random()))

class JsonGenerator:
	def __init__(self, json_path):
		self.points = []
		c = json.loads(open(json_path, 'rb').read())
		for row in c:
			self.points.append((float(row['lat']), float(row['lng'])))
