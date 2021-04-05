import re


def read_parameters():
    """
    Reads the information about an auction from a file.
    Parameters and bidder % are separated for ease when it comes to creating the bidders.

    :return: number_of_rounds: the number of rounds
    parameters: the parameters of the auction
    bidders: the bidder types and their percentages.
    """
    number_of_rounds = 0

    parameters = {
        "Number of Bidders": 0,
        "Auction Types": '',
        "Reserve Price": 0.0,
        "Starting Bid": 0.0,
        "Auctioneer Type": ''
    }

    bidders = {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0
    }

    simulator = {
        "Number of Rounds": 0,
        "Data Type": '',
        "Agent Type": '',
        "Number of Agent Types": 0
    }

    pattern = r'((\w+ )*\w+) = ((\(t\d,t\d\)(,\(t\d,t\d\))*)|([ABCD](,[ABCD])*)|\d+|\w+|(\'(\w+ )*\w+\'))'

    with open("auction.txt", "r") as auction_info:

        for line in auction_info:
            line = line.rstrip()

            # Empty lines and comment lines (starting with '#') are ignored.
            if '#' in line or len(line) == 0:
                continue

            # The regex is looking for the shape 'name = value'
            result = re.search(pattern, line)
            name = result.group(1)
            value = result.group(3)

            # Depending on which dictionary it belongs to, it'll be added based on the 'name' part
            if name in bidders.keys():
                bidders[name] = float(value)
                continue

            # There are certain values that must be converted to either int or float
            if name == 'Auction Types':
                parameters[name] = value
            elif name == 'Auctioneer Type':
                parameters[name] = list(value.split(','))
            elif name == 'Number of Bidders':
                parameters[name] = int(value)
            elif name == "Number of Rounds" or name == "Number of Agent Types":
                simulator[name] = int(value)
            elif name in simulator.keys():
                simulator[name] = value.replace('\'', '')
            else:
                parameters[name] = float(value)

        return simulator, parameters, bidders
