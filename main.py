"""The main file."""

import time
from datetime import datetime
from auction import *
import data_analyser as da
import agents_factory as af
import metrics_writer as mw
import parameters_reader as pr


def extract_information():
    global file_name, headers, simulator, parameters, bidders, auctioneer_types, auction_types

    # These are the headers they correspond to in terms of how the auction is coded.
    headers = ('Auction Types', 'Auctioneer Type', 'A', 'B', 'C', 'D', 'Winner Type', 'Starting Bid', 'Revenue',
               'Winner Satisfaction', 'Auctioneer Satisfaction', 'Social Welfare', 'Efficiency', 'Speed')

    # Get the information from the .txt file
    simulator, parameters, bidders = pr.read_parameters(headers)
    auctioneer_types = parameters["Auctioneer Type"]
    auction_types = parameters["Auction Types"].split(',')

    # Set the file name for the metrics
    today = datetime.today()
    file_name = "metrics " + today.strftime('%d-%m-%y') + ".csv"


def run_simulation():
    global agents_factory
    mw.write_metrics(headers, file_name)

    # Start the counter and begin the simulation
    start = time.time()
    list_of_auctions = []
    for counter in range(0, simulator["Number of Rounds"]):
        # For every type of auction, we must use the same bidders
        agents_factory = af.AgentsFactory(parameters, bidders)

        # For every auctioneer type, we will use the same bidders but with updated budget and a new auctioneer
        for auctioneer_type in auctioneer_types:
            parameters["Auctioneer Type"] = auctioneer_type

            agents_factory.create_auctioneer(parameters)

            # Loop dealing with all the different auction types
            for auction_combination in auction_types:
                parameters["Auction Types"] = auction_combination

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
    print("I am done with the models! It took {0} seconds.\n The information is saved in the file '{1}'.".format(end - start, file_name))


def analyse_data():
    # Since the data can be simulated from different aspects, we need to make sure the labels for the agents will be correct
    data_type = simulator["Data Type"]
    agent_type = simulator["Agent Type"]
    types = {"Winner Type": ["A", "B", "C", "D"]}
    if "Auctioneer Type" in agent_type:
        types["Auctioneer Type"] = auctioneer_types
    if "Auction Types" in agent_type:
        types["Auction Types"] = auction_types
    da.analyse_data(file_name, list(data_type.split(',')), list(agent_type.split(',')), types)


if __name__ == "__main__":
    extract_information()
    run_simulation()
    analyse_data()
