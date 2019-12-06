import numpy as np
from creator import Creator
from viewer import Viewer
from advertiser import Advertiser
from operator import itemgetter

np.random.seed(0)

# creating players
num_creators = 3
num_advertisers = 3
num_viewers = 3

creators = [Creator(i, 5, 1000) for i in range(num_creators)]
advertisers = [Advertiser(i, 1000, num_creators) for i in range(num_advertisers)]
viewers = [Viewer(i, 100, num_creators) for i in range(num_viewers)]

rounds = 2
prev_bids = None
prev_prices = [None] * num_creators

for c in creators:
	print "hi"

for i in range(rounds):
	# create bid list from all advertisers and viewers
	# keep track of where bids are coming from
	current_bids = []

	# this is list of (advertiser_id, bidlst)
	# bidlst is [(creator_id, bid, amount)]
	advertiser_bids = []
	for advertiser in advertisers:
		advertiser_bids.append((advertiser.id,advertiser.bids(creators)))

	# this is list of (viewer_id, bidlst)
	# bidlst is [(creator_id, bid, amount)]
	viewer_bids = []
	for viewer in viewers:
		viewer_bids.append((viewer.id,viewer.bids(prev_prices, creators)))

	# creates list of bid lists sorted by coin
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

	# create ask list from all creators and viewers
	# keep track of where asks are coming from
	current_asks = []

	# this is list of (creator_id, asklst)
	# asklst is [(creator_id, ask, amount)]
	creator_asks = []
	for creator in creators:
		creator_asks.append((creator.id,creator.asks(prev_bids, advertisers)))

	# this is list of (viewer_id, asklst)
	# asklst is [(creator_id, ask, amount)]
	viewer_asks = []
	for viewer in viewers:
		viewer_asks.append((viewer.id,viewer.asks(prev_prices, creators)))

	# creates list of ask lists sorted by coin
	for c_id in range(num_creators):
		asks_on_c = []
		for viewer_id, alist in viewer_asks:
			for ask in alist:
				if ask[0] == c_id:
					asks_on_c.append( (ask[0], ask[1], ask[2], 'v', viewer_id) )

		for creator_id, alist in creator_asks:
			for ask in alist:
				if ask[0] == c_id:
					asks_on_c.append( (ask[0], ask[1], ask[2], 'c', creator_id) )
		current_asks.append(asks_on_c)

	def get_batch_price(sorted_bids, sorted_asks, prev_price):
		if not sorted_bids or not sorted_asks or sorted_bids[0][1] < sorted_asks[0][1]:
			return prev_price
		elif sorted_bids[0][2] == 0:
			return get_batch_price(sorted_bids[1:], sorted_asks, prev_price)
		else:
			if sorted_bids[0][2] == sorted_asks[0][2]:
				return get_batch_price(sorted_bids[1:], sorted_asks[1:], np.average([sorted_bids[0][1],sorted_asks[0][1]]))
			
			elif sorted_bids[0][2] < sorted_asks[0][2]:
				new_asks = [(sorted_asks[0][0], sorted_asks[0][1], sorted_asks[0][2] - sorted_bids[0][2], sorted_asks[0][3], sorted_asks[0][4])] + sorted_asks[1:]
				return get_batch_price(sorted_bids[1:], new_asks, np.average([sorted_bids[0][1],sorted_asks[0][1]]))
			
			elif sorted_bids[0][2] > sorted_asks[0][2]:
				new_bids = [(sorted_bids[0][0], sorted_bids[0][1], sorted_bids[0][2] - sorted_asks[0][2], sorted_bids[0][3], sorted_bids[0][4])] + sorted_bids[1:]
				return get_batch_price(new_bids, sorted_asks[1:], np.average([sorted_bids[0][1],sorted_asks[0][1]]))

	def get_batch_transactions(sorted_bids, sorted_asks, transactions):
		if not sorted_bids or not sorted_asks or sorted_bids[0][1] < sorted_asks[0][1]:
			return transactions
		elif sorted_bids[0][2] == 0:
			return get_batch_transactions(sorted_bids[1:], sorted_asks, transactions)
		else:
			a_type = sorted_asks[0][3]
			a_id = sorted_asks[0][4]
			b_type = sorted_bids[0][3]
			b_id = sorted_bids[0][4]
			if sorted_bids[0][2] == sorted_asks[0][2]:
				amount = sorted_bids[0][2]
				transactions.append( (a_type,a_id,b_type,b_id,amount) )
				return get_batch_transactions(sorted_bids[1:], sorted_asks[1:], transactions)
			elif sorted_bids[0][2] < sorted_asks[0][2]:
				amount = sorted_bids[0][2]
				transactions.append( (a_type,a_id,b_type,b_id,amount) )
				new_asks = [(sorted_asks[0][0], sorted_asks[0][1], sorted_asks[0][2] - sorted_bids[0][2], sorted_asks[0][3], sorted_asks[0][4])] + sorted_asks[1:]
				return get_batch_transactions(sorted_bids[1:], new_asks, transactions)
			
			elif sorted_bids[0][2] > sorted_asks[0][2]:
				amount = sorted_asks[0][2]
				transactions.append( (a_type,a_id,b_type,b_id,amount) )
				new_bids = [(sorted_bids[0][0], sorted_bids[0][1], sorted_bids[0][2] - sorted_asks[0][2], sorted_bids[0][3], sorted_bids[0][4])] + sorted_bids[1:]
				return get_batch_transactions(new_bids, sorted_asks[1:], transactions)
	

	# for each coin: match bid list and ask list
	for c_id in range(num_creators):
		bids_on_c = current_bids[c_id]
		asks_on_c = current_asks[c_id]
		# sort bids descending (on second value)
		sorted_bids = sorted(bids_on_c, key=itemgetter(1), reverse=True)
		# sort asks ascending
		sorted_asks = sorted(asks_on_c, key=itemgetter(1))
		
		# match pairs one by one to find batch price
		batch_price = get_batch_price(sorted_bids, sorted_asks, None)

		transactions = get_batch_transactions(sorted_bids,sorted_asks,[])

		# populate prev_prices[coin] to be the batch price
		# if no batch price then prev_prices stays the same
		if batch_price:
			prev_prices[c_id] = batch_price
			
		# go through matched pairs, for each match:
		for t in transactions:
			coin_amount = t[4]
			# take away matched coin from asker, give them USD corresponding to matched coin * median price
			# update wallet
			a_type = t[0]
			a_id = t[1]
			if a_type == 'v':
				viewers[a_id].update_wallet(c_id, batch_price, -coin_amount)
				viewers[a_id].budget += coin_amount*batch_price
			elif a_type == 'c':
				creators[a_id].coins -= coin_amount
				creators[a_id].usd += coin_amount*batch_price
			
			# take away matched USD corresponding to matched coin times median price from bidder and give them coin
			# update wallet
			b_type = t[2]
			b_id = t[3]
			if b_type == 'v':
				viewers[b_id].update_wallet(c_id, batch_price, coin_amount)
				viewers[b_id].budget -= coin_amount*batch_price
			elif b_type == 'a':
				advertisers[b_id].update_wallet(c_id, batch_price, coin_amount)
				advertisers[b_id].budget -= coin_amount*batch_price

	# let advertisers run ads
	for a in advertisers:
		a.buy_ad(creators)

	# update creator popularities
	for c in creators:
		c.next_index()

	prev_bids = current_bids
