import numpy as np

class Viewer:
	def __init__(self, id, budget, num_creators):
		self.id = id # 0 through V
		self.budget = budget
		self.wallet = [[0 for i in range(2)] for j in range(num_creators)] # [amount, avg price paid]
		self.match_vals = np.random.rand(num_creators).tolist()
		self.pref_order = np.argsort(self.match_vals)[::-1]

	# returns list of triples (creator, bid, amount)
	def bids(self, prev_prices, creators):
		curr_budget = self.budget
		bid_lst = []
		for index in self.pref_order:
			if prev_prices[index]:
				bid = prev_prices[index]*creators[index].popularity()/creators[index].prev_popularity
				amount = np.random.uniform(0,curr_budget/bid)
				bid_lst.append((index, bid, amount))
				curr_budget -= bid*amount
		return bid_lst

	# returns list of triples (creator, ask price, amount)
	def asks(self, prev_prices, creators):
		ask_lst = []
		for i in range(len(self.wallet)):
			if self.wallet[i][0]:
				price_belief = prev_prices[i]*creators[i].popularity()/creators[i].prev_popularity
				if price_belief > self.wallet[i][1]:
					if np.random.uniform(0,1) < np.exp(-self.match_vals[i]):
						ask_lst.append((i, price_belief,self.wallet[i][0]))
				else:
					continue
			else:
				pass
		return ask_lst

	# creator_id is equivalent to coin_id
	def update_wallet(self, creator_id, price, amount):
		if amount > 0:
			self.wallet[creator_id][1] = (self.wallet[creator_id][0] * self.wallet[creator_id][1] + price * amount) / (self.wallet[creator_id][0] + amount)
		self.wallet[creator_id][0] += amount

	def approx_val(self, prev_prices):
		prev_prices = [p if p else 0 for p in prev_prices]
		return self.budget + sum([self.wallet[i][0]*prev_prices[i] for i in range(len(self.wallet))])
