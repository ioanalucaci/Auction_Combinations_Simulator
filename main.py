import matplotlib.pyplot as plt
from auction import *

# TODO: Get the output in a csv file (or excel spreadsheet file)
# TODO: Work on connecting the .txt file with the main file
# GNU plot(?) and vectorised plots

model = Auction(1000, ['t2','t1'], 70, 50, 'a1', {'b1': 10, 'b2': 30, 'b3': 40, 'b4': 20})

model.step()
