
import random

class WhiteNoiseGenerator:
	def __init__(self, n):
		self.points = []
		for i in range(n):
			self.points.append((random.random(),random.random()))
