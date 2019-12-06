import numpy as np

class Creator(id, max_p, total_coin):
	self.id = id # 0 through C
	self.usd = 0
	self.coins = total_coin
	self.max_p = max_p
	self.pop_index = 0
	self.low, self.high = -0.05, 0.1
	self.prev_popularity = None

	def popularity():
		return self.max_p/(1+np.exp(-self.pop_index/self.max_p))

	def next_index():
		self.prev_popularity = self.popularity()
		self.pop_index += np.random.uniform(self.low,self.high)

	def asks(prev_round, bidders):
		if prev_round == None:

		else:
