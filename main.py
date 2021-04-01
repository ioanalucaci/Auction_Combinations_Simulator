from auction import *
import metrics_writer as mw
import parameters_reader as pr
import data_visualiser as da
import time
from datetime import datetime

# TODO: Look into BatchRunner
# TODO: Look into DataCollector
# https://mesa.readthedocs.io/en/stable/tutorials/intro_tutorial.html

list_of_auctions = []
start = time.time()

number_of_rounds, parameters, bidders = pr.read_parameters()

for counter in range(0, number_of_rounds):
    model = Auction(parameters, bidders)
    model.step()
    list_of_auctions.append(model)
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++")

end = time.time()

print("I am done with the models! It took {0}".format(end - start))

mw.write_metrics(list_of_auctions)

print("Writing took {0}".format(time.time() - end))

today = datetime.today()

file_name = "metrics " + today.strftime('%d-%m-%y') + ".csv"

da.visualise_data("Winner Type", "Auctioneer Satisfaction", file_name)
