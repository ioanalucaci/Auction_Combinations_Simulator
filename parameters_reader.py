"""Functions in charge of reading the auction.txt file"""
import re


def read_parameters(headers):
    """
    Reads the information about an auction from a file.
    Parameters and bidder % are separated for ease when it comes to creating the bidders.

    :parameter headers: The headers that will be published in the csv file.
    :return: simulator: The information for the simulator.
             parameters: The parameters of the auction
             bidders: The bidder types and their percentages.
    """

    # Declaration of all the information we need
    parameters = {"Number of Bidders": None, "Auction Types": None, "Reserve Price": None, "Auctioneer Type": None}
    bidders = {"A": 0, "B": 0, "C": 0, "D": 0}
    simulator = {"Number of Rounds": None, "Data Type": None, "Agent Type": None}

    # Populate the dictionaries that need to be returned
    with open("auction.txt", "r") as auction_info:

        for line in auction_info:
            line = line.rstrip()
            # Empty lines and comment lines (starting with '#') are ignored.
            if '#' in line or len(line) == 0:
                continue

            # The regex is looking for the shape 'name = value'
            pattern = r'((\w+ )*\w+) = (([EDVF]{1,2}(,[EDVF]{1,2})*)|([ABCD](,[ABCD])*)|\d+|(\'(\w+ )*\w+\')(,\'(\w+ )*\w+\')*)'
            result = re.search(pattern, line)
            try:
                name = result.group(1)
                value = result.group(3)
            except Exception as e:
                raise Exception(
                    "The data could not be parsed. Error raised at the following line: \"{0}\"".format(line), e)
            if result.group(0) is not line:
                raise Exception(
                    "The data could not be parsed. Error raised at the following line: \"{0}\"".format(line))

            format_data(line, name, value, parameters, simulator, bidders)

    check_information(bidders, headers, parameters, simulator)

    return simulator, parameters, bidders


def format_data(line, name, value, parameters, simulator, bidders):
    """
    Formats the data in the correct dictionary.

    :param line: The line currently being checked
    :param name: The name of the 'name = value' pair
    :param value: The value of the 'name = value' pair
    :param parameters: The parameters dictionary
    :param simulator: The simulator dictionary
    :param bidders: The bidders dictionary
    :return:
    """
    # Depending on which dictionary it belongs to, it'll be added based on the 'name' part
    if name in bidders.keys():
        bidders[name] = float(value)
        return

    # There are certain values that must be converted to either int or float
    try:
        if name == 'Auction Types':
            parameters[name] = value
        elif name == 'Auctioneer Type':
            parameters[name] = list(value.split(','))
        elif name == 'Number of Bidders':
            parameters[name] = int(value)
        elif name == "Number of Rounds":
            simulator[name] = int(value)
        elif name in simulator.keys():
            simulator[name] = value.replace('\'', '')
        else:
            parameters[name] = float(value)
    except Exception as e:
        raise Exception("The data could not be parsed. Error raised at the following line: \"{0}\"".format(line), e)


def check_information(bidders, headers, parameters, simulator):
    """
    Checks that all of the information is present.

    :param bidders: The bidder types and their percentages.
    :param headers: The headers that will be published in the csv file.
    :param parameters: The parameters of the auction
    :param simulator: The data for the simulator.
    :return:
    """
    if None in simulator.values() or None in parameters.values():
        list_of_missing = []
        for name, value in simulator.items():
            if value is None:
                list_of_missing.append(name)
        for name, value in parameters.items():
            if value is None:
                list_of_missing.append(name)
        raise Exception("Incomplete information. You are missing: {0}".format(list_of_missing))

    # Check that bidders add up to 100
    if sum(bidders.values()) != 100:
        raise Exception("Bidders percentages must add up to 100.")

    # Check that we will look for data for the graphs that exists in the file.
    for agent_type in simulator['Agent Type'].split(','):
        if agent_type not in headers:
            raise Exception("Agent type {0} not present in the csv file.".format(agent_type))
    for data_type in simulator['Data Type'].split(','):
        if data_type not in headers:
            raise Exception("Data type {0} not present in the csv file.".format(data_type))
