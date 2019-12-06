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

	# prev_bids is list of bid_lsts (list of triples)
	def asks(prev_bids, bidders):
		if prev_bids == None:
			accum = 0
			for bidder in bidders:
				accum += bidder.val_to_bid(0.25*self.popularity())
			return accum/len(bidders)
		else:
			my_prev_bids = []
			for bid_lst in prev_bids:
				for bid in bid_lst:
					if bid[0] == self.id:
						# bid = (creator, bid price, amount)
						my_prev_bids.append(bid[1])
			return np.average(my_prev_bids)*self.popularity()/self.prev_popularity