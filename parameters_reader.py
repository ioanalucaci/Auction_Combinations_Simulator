import re


def read_parameters(headers):
    """
    Reads the information about an auction from a file.
    Parameters and bidder % are separated for ease when it comes to creating the bidders.

    :parameter headers: The headers that will be published in the csv file.
    :return: number_of_rounds: the number of rounds
             parameters: the parameters of the auction
             bidders: the bidder types and their percentages.
    """

    # Declaration of all the information we need
    parameters = {
        "Number of Bidders": None,
        "Auction Types": None,
        "Reserve Price": None,
        "Auctioneer Type": None
    }

    bidders = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0
    }

    simulator = {
        "Number of Rounds": None,
        "Data Type": None,
        "Agent Type": None
    }

    pattern = r'((\w+ )*\w+) = ((\(t[1234](,t[1234]){0,1}\)(,\(t[1234](,t[1234])*\))*)|([ABCD](,[ABCD])*)|\d+|(\'(\w+ )*\w+\'))'

    # Populate the dictionaries that need to be returned
    with open("auction.txt", "r") as auction_info:

        for line in auction_info:
            line = line.rstrip()

            # Empty lines and comment lines (starting with '#') are ignored.
            if '#' in line or len(line) == 0:
                continue

            # The regex is looking for the shape 'name = value'
            result = re.search(pattern, line)
            try:
                name = result.group(1)
                value = result.group(3)
            except Exception as e:
                raise Exception("The data could not be parsed. Error raised at the following line: \"{0}\"".format(line), e)

            if result.group(0) is not line:
                raise Exception("The data could not be parsed. Error raised at the following line: \"{0}\"".format(line))

            # Depending on which dictionary it belongs to, it'll be added based on the 'name' part
            if name in bidders.keys():
                bidders[name] = float(value)
                continue

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

    # Check that all of the information is present
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
    if simulator['Data Type'] not in headers or simulator['Agent Type'] not in headers:
        raise Exception("Agent and/or Data type not present in the csv file.")

    return simulator, parameters, bidders
