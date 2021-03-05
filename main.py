import matplotlib.pyplot as plt
from auction import *

model = Auction(10, 't1t2', 50, 'a1', {'b1': 20, 'b2': 30, 'b3': 40, 'b4': 10})

model.step()
