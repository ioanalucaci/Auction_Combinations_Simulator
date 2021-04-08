from auction import *
import metrics_writer as mw
import parameters_reader as pr
import data_analyser as da
import time


list_of_auctions = []
start = time.time()

simulator, parameters, bidders = pr.read_parameters()

auctioneer_types = parameters["Auctioneer Type"]
auction_types = parameters["Auction Types"].split('),(')

for auctioneer_type in auctioneer_types:
    parameters["Auctioneer Type"] = auctioneer_type

    for auction_combination in auction_types:
        parameters["Auction Types"] = auction_combination.replace('(', '').replace(')', '')

        for counter in range(0, simulator["Number of Rounds"]):
            model = Auction(parameters, bidders)
            model.step()
            list_of_auctions.append(model)

end = time.time()

print("I am done with the models! It took {0}".format(end - start))

file_name = mw.write_metrics(list_of_auctions)

print("Writing took {0}".format(time.time() - end))

data_type = simulator["Data Type"]
agent_type = simulator["Agent Type"]
types = ["A", "B", "C", "D"]

if agent_type == "Auctioneer Type":
    types = auctioneer_types

if agent_type == "Auction Types":
    types = [auction_type.replace("(", "").replace(")", "") for auction_type in auction_types]

da.analyse_data(file_name, data_type, agent_type, types)
