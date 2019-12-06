import numpy as np

class Viewer:
	def __init__(self, id, budget, num_creators):
		self.id = id
		self.budget = budget
		self.wallet = [[0,0]] * num_creators # [amount, avg price paid]
		self.match_vals = np.random.rand(num_creators).tolist()
		self.pref_order = np.argsort(self.match_vals)[::-1]

	# returns list of triples (creator, bid, amount)
	def bids(self, prev_prices, creators):
		curr_budget = self.budget
		bid_lst = []
		for index in self.pref_order:
			bid = prev_prices[index]*creators[index].popularity()/creators[index].prev_popularity
			amount = np.random.uniform(0,curr_budget/bid)
			bid_lst.append((index, bid, amount))
			curr_budget -= bid*amount
		return bid_lst


	# returns list of triples (creator, ask price, amount)
	def asks(self, prev_prices, creators):
		ask_lst = []
		for i in range(len(self.wallet)):
			price_belief = prev_prices[index]*creators[index].popularity()/creators[index].prev_popularity
			if price_belief > self.wallet[i][1]:
				if np.random.uniform(0,1) < np.exp(-self.match_vals[i]):
					ask_lst.append((i, price_belief,self.wallet[i][0]))
			else:
				pass
		return ask_lst