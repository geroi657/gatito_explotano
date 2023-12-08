from pygame import *

class CheatCodeHandler:
	def __init__(self):
		self.codes = [
			[],
			[K_UP, K_UP, K_DOWN, K_DOWN, K_LEFT, K_RIGHT, K_LEFT, K_RIGHT, K_b, K_a, K_RETURN]
		]
		self.counts = [0 for _ in self.codes]

	def handle(self, keycode):
		for i in range(1, len(self.codes)):
			c = self.counts[i]
			target_key = self.codes[i][c]
			if keycode == target_key:
				self.counts[i] += 1
			else:
				self.counts[i] = 0
			if self.counts[i] == len(self.codes[i]):
				self.counts[i] = 0
				return i
		return False
