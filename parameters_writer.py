"""
Functions in charge of writing the parameters.
"""


def write_simulation_information(number_of_rounds, data_type, agent_type):
    """Writes the simulation information in the input file.

    :param number_of_rounds: The number of rounds
    :param data_type: The type of data
    :param agent_type: The type of agent
    """

    auction_file = open("auction.txt", "w")

    data_result = f"'{data_type[0]}'"
    for counter in range(1, len(data_type)):
        data_result = data_result + ",'{0}'".format(data_type[counter])

    agent_result = f"'{agent_type[0]}'"
    for counter in range(1, len(agent_type)):
        agent_result = agent_result + ",'{0}'".format(agent_type[counter])

    result = f"# Simulation\nNumber of Rounds = {number_of_rounds}\nData Type = {data_result}\nAgent Type = {agent_result}\n\n"
    auction_file.write(result)


def write_auction_information(number_of_bidders, auction_types, reserve_price, auctioneer_type):
    """ Writes the auction information in the input file.

    :param number_of_bidders: The number of bidders
    :param auction_types: The auction types
    :param reserve_price: The reserve price
    :param auctioneer_type: The auctioneer type
    """
    auction_file = open("auction.txt", "a")
    result = f"# Auction\nNumber of Bidders = {number_of_bidders}\nAuction Types = {auction_types}\nReserve Price = {reserve_price}\nAuctioneer Type = {auctioneer_type}\n\n"
    auction_file.write(result)


def write_bidders_percentages(bidder_a, bidder_b, bidder_c, bidder_d):
    """ Writes the percentages of bidders in the input file.

    :param bidder_a: The percentage of bidders of type A
    :param bidder_b: The percentage of bidders of type B
    :param bidder_c: The percentage of bidders of type C
    :param bidder_d: The percentage of bidders of type D
    """
    auction_file = open("auction.txt", "a")
    result = f"# Bidders' Type Percentages\nA = {bidder_a}\nB = {bidder_b}\nC = {bidder_c}\nD = {bidder_d}\n"
    auction_file.write(result)
