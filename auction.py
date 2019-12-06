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
prev_prices = [None] * num_creators

for i in range(rounds):
	# create bid list from all advertisers and viewers
	# keep track of where bids are coming from
	current_bids = []

	# this is list of (advertiser_id, bidlst)
	# bidlst is [(creator_id, bid, amount)]
	advertiser_bids = []
	for advertiser in advertisers:
		advertiser_bids.append((advertiser.id,advertiser.bids()))

	viewer_bids = []
	for viewer in viewers:
		viewer_bids.append((viewer.id,viewer.bids()))


	for c_id in range(num_creators):
		bids_on_c = []
		for viewer_id, blist in viewer_bids:
			for bid in blist:
				if bid[0] == c_id:
					bids_on_c.append( (bid[0],bid[1],bid[2],'v',viewer_id) )

		for advertiser_id, blist in advertiser_bids:
			for bid in blist:
				if bid[0] == c_id:
					bids_on_c.append( (bid[0],bid[1],bid[2],'a',advertiser_id))
		current_bids.append(bids_on_c)


	current_asks = []
	# create ask list from all creators and viewers
	# keep track of where asks are coming from

	# for each coin: match bid list and ask list
		# sort bids and asks in the correct order
		# match pairs one by one to find batch price
		# populate prev_prices[coin] to be the batch price
			# if no batch price then prev_prices stays the same
		# go through matched pairs, for each match:
			# take away matched coin from asker, give them USD corresponding to matched coin * median price
			# take away matched USD corresponding to matched coin times median price from bidder and give them coin
			# update wallet amt for bidders (also avg price) and askers


	# let advertisers run ads

	# update creator popularities

	prev_bids = current_bids
