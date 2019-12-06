import numpy as np

class Advertiser:
  def __init__(self, id, budget, num_creators):
    self.id = id
    self.budget = budget
    self.wallet = [[0,0]] * num_creators # [amount, avg price paid]
    self.quality = np.random.uniform(0,1)
    self.match_vals = np.random.rand(num_creators).tolist()
    self.num_creators = num_creators

  # take in creator_id, and value and return
  # bid price
  def val_to_bid(self, value):
    return 2/3 * value

  # use function above and some logic to return
  # tuple of creator_id, bid, and amount
  def bid_strategy(self, cv_tuple):
    bid_lst = []
    rand_index = np.random.randint(0,self.num_creators)
    for index, value in cv_tuple:
      price = self.val_to_bid(value)
      if index == rand_index:
        quantity = self.budget/price
      else:
        quantity = 0
      full_tuple = (index, price, quantity)
      bid_lst.append(full_tuple)
    return bid_lst

  # call the above function to return list of bids
  def bids(self, creators):
    cv_tuple = []
    for creator in creators:
      pop = creator.popularity()
      v = self.match_vals[creator.id]
      q = self.quality
      E = pop * v * q
      cv_tuple.append((creator.id,E))
    return self.bid_strategy(cv_tuple)

  def buy_ad(self, creators):
    for i in range(len(self.wallet)):
      E = creators[i].popularity() * self.quality * self.match_vals[i]
      if self.wallet[i][1] > E:
        pass
      else:
        self.budget += E*self.wallet[i][0]
        creators[i].coins += self.wallet[i][0]
        self.wallet[i] = [0,0]

  def asks(self):
    pass




