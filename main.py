import matplotlib.pyplot as plt
from auction import *
import metrics_writer
import time

# TODO: Work on connecting the .txt file with the main file
# GNU plot(?) and vectorised plots

list_of_auctions = []
start = time.time()


for x in range(0, 1000):
    model = Auction(100, ['t1', 't2'], 55, 50, 'a', {'a': 25, 'b': 25, 'c': 25, 'd': 25})
    model.step()
    list_of_auctions.append(model)
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
end = time.time()

print("I am done with the models! It took {0}".format(end - start))

metrics_writer.write_metrics('metrics.csv', list_of_auctions)

print("Writing took {0}".format(time.time() - end))
