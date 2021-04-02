from auction import *
import metrics_writer as mw
import parameters_reader as pr
import time


list_of_auctions = []
start = time.time()

number_of_rounds, parameters, bidders = pr.read_parameters()

auctioneer_types = parameters["Auctioneer Type"]

for auctioneer_type in auctioneer_types:
    parameters["Auctioneer Type"] = auctioneer_type
    for counter in range(0, number_of_rounds):
        model = Auction(parameters, bidders)
        model.step()
        list_of_auctions.append(model)
        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++")


end = time.time()

print("I am done with the models! It took {0}".format(end - start))

mw.write_metrics(list_of_auctions)

print("Writing took {0}".format(time.time() - end))
