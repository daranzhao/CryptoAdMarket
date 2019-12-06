import numpy as np

class Viewer(id, budget, num_creators):
	self.id = id
	self.budget = budget
	self.wallet = [0] * num_creators
	self.match_vals = np.random.rand(num_creators).tolist()

	