import time
from auction import *
import data_analyser as da
import agents_factory as af
import metrics_writer as mw
import parameters_reader as pr

list_of_auctions = []

# These are the headers they correspond to in terms of how the auction is coded.
headers = ('Auction Types', 'Auctioneer Type', 'A', 'B', 'C', 'D', 'Winner Type', 'Starting Bid', 'Revenue',
           'Winner Satisfaction', 'Auctioneer Satisfaction', 'Social Welfare', 'Efficiency', 'Round No')

# Get the information from the .txt file
simulator, parameters, bidders = pr.read_parameters(headers)

auctioneer_types = parameters["Auctioneer Type"]
auction_types = parameters["Auction Types"].split('),(')
file_name = mw.write_metrics(headers)

# Start the counter and begin the simulation
start = time.time()

for counter in range(0, simulator["Number of Rounds"]):
    # For every type of auction, we must use the same bidders
    agents_factory = af.AgentsFactory(parameters, bidders)

    # For every auctioneer type, we will use the same bidders but with updated budget and a new auctioneer
    for auctioneer_type in auctioneer_types:
        parameters["Auctioneer Type"] = auctioneer_type

        agents_factory.create_auctioneer(parameters)

        # Loop dealing with all the different auction types
        for auction_combination in auction_types:
            parameters["Auction Types"] = auction_combination.replace('(', '').replace(')', '')

            agents_factory.update_prices(parameters["Auction Types"])

            model = Auction(parameters, bidders, agents_factory)
            model.step()
            list_of_auctions.append(model)

    # To avoid caching everything for big number of simulations, we will write every 500 rounds in the .csv file
    if len(list_of_auctions) > 500:
        mw.write_simulators(file_name, list_of_auctions, headers)
        list_of_auctions = []

# To avoid losing any information, we need to check at the end that we wrote every round
if len(list_of_auctions) > 0:
    mw.write_simulators(file_name, list_of_auctions, headers)

end = time.time()

print("I am done with the models! It took {0}".format(end - start))

# Since the data can be simulated from different aspects, we need to make sure the labels for the agents will be correct
data_type = simulator["Data Type"]
agent_type = simulator["Agent Type"]
types = {"Winner Type": ["A", "B", "C", "D"]}

if "Auctioneer Type" in agent_type:
    types["Auctioneer Type"] = auctioneer_types

if "Auction Types" in agent_type:
    types["Auction Types"] = [auction_type.replace("(", "").replace(")", "") for auction_type in auction_types]

da.analyse_data(file_name, list(data_type.split(',')), list(agent_type.split(',')), types)
