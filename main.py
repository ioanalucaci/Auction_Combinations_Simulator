import matplotlib.pyplot as plt
from auction import *

# TODO: Get the output in a csv file (or excel spreadsheet file)
# TODO: Work on connecting the .txt file with the main file
# GNU plot(?) and vectorised plots

model = Auction(1000, ['t2','t1'], 70, 50, 'a', {'a': 10, 'b': 30, 'c': 40, 'd': 20})

model.step()
