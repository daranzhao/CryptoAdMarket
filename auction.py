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

for i in range(rounds):
	# 
