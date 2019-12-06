import numpy as np
from creator import Creator
from viewer import Viewer
from advertiser import Advertiser

np.random.seed(0)

# creating players
num_creators = 3
num_advertisers = 3
num_viewers = 3

creators = [Creator(i, 5, 1000) for i in range(num_creators)]
advertisers = [Advertiser(i, 1000, num_creators) for i in range(num_advertisers)]
viewers = [Viewer(i, 100, num_creators) for i in range(num_viewers)]

rounds = 25
prev_bids = None
prev_prices = None

for i in range(rounds):
	# create bid list from all advertisers and viewers
	# keep track of where bids are coming from

	# create ask list from all creators and viewers
	# keep track of where asks are coming from

	# for each coin: match bid list and ask list
		# sort bids and asks in the correct order
		# match pairs one by one to find batch price
		# go through matched pairs, for each match:
			# take away matched coin from asker, give them USD corresponding to matched coin * median price
			# take away matched USD corresponding to matched coin times median price from bidder and give them coin
			# update wallet amt for bidders (also avg price) and askers

	# let advertisers run ads

	# update creator popularities
