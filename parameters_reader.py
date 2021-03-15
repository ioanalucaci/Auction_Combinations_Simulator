import re


# TODO: Add exception handling in case there's a problem with a .txt file, e.g. people forget to complete the info
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
        "a": 0,
        "b": 0,
        "c": 0,
        "d": 0
    }

    pattern = r'((\w+ )*\w+) = ((t\d,t\d)|\d+|\w+)'

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

            if name not in parameters.keys():
                number_of_rounds = int(value)
                continue

            # There are certain values that must be converted to either int or float
            if name == 'Auctioneer Type' or name == 'Auction Types':
                parameters[name] = value
            elif name == 'Number of Bidders':
                parameters[name] = int(value)
            else:
                parameters[name] = float(value)

        return number_of_rounds, parameters, bidders
