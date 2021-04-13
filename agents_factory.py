import random


class AgentsFactory:
    """Class in charge of creating the agents."""
    def __init__(self, parameters, bidder_types):
        """
        The initialising function.

        :param parameters: The agents' parameters
        :param bidder_types: The bidder types
        """
        self.auctioneer = {}

        # Create bidders
        number_of_bidders = parameters["Number of Bidders"]

        self.bidders = []

        # For every type, we see how many we have to create
        for bidder_type in bidder_types.keys():
            number_of_bidders_type = int(bidder_types[bidder_type] * number_of_bidders / 100)

            # We create the number of bidders for a specific type
            for counter in range(number_of_bidders_type):
                budget = 0

                risk = round(random.uniform(0.1, 0.99), 1)
                base_rate = round(random.uniform(0.01, 0.1), 2)
                utility = round(random.uniform(0.1, 0.99), 1)
                bidder_information = (risk, base_rate, utility)

                self.bidders.append(
                    {
                        "budget": budget,
                        "bidder_type": bidder_type,
                        "bidder_information": bidder_information
                    }
                )

    def create_auctioneer(self, parameters):
        """
        Creates a new auctioneer.

        :param parameters: parameters for the new auctioneer.
        """
        # Create auctioneer
        reserve_price = parameters["Reserve Price"]
        base_rate = round(random.uniform(0.05, 0.3), 2)

        self.auctioneer = {"starting_bid": 0, "reserve_price": reserve_price,
                           "auctioneer_type": parameters["Auctioneer Type"],
                           "base_rate": base_rate}

    def update_prices(self, current_auction):
        """
        Updates the budget and starting price depending on the auction type.

        :param current_auction: the current auction type
        :return:
        """
        current_auction = list(current_auction.split(','))[0]
        base_rate = self.auctioneer["base_rate"]
        reserve_price = self.auctioneer["reserve_price"]

        # Update auction starting bid
        starting_bid = reserve_price * (1 + base_rate)

        if current_auction == 't2':
            multiplier = round(random.uniform(1.3, 2), 1)
            starting_bid = reserve_price * (multiplier + base_rate)

        if current_auction == 't1':
            multiplier = round(random.uniform(1, 1.03), 1)
            starting_bid = reserve_price * multiplier

        self.auctioneer["starting_bid"] = starting_bid

        # Update bidders' budgets
        updated_bidders = []

        for bidder in self.bidders:
            bidder["budget"] = random.randint(int(reserve_price * 1.1), int(reserve_price * 1.3))
            updated_bidders.append(bidder)

        self.bidders = updated_bidders
