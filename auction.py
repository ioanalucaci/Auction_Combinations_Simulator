"""
The auction class for the simulation.
"""
import random
from mesa import Model
from mesa.time import SimultaneousActivation
from bidder import Bidder
from auctioneer import Auctioneer


class Auction(Model):
    """Model that simulates an auction situation. Used to dictate the communication between auctioneers and bidders."""

    def __init__(self, parameters, bidder_types):
        """
        Initialisation function for the auction model.

        :param parameters: all the required parameters for the auction.
        :param bidder_types: the types of bidders to join this auction alongside their percentage
        """

        super().__init__()
        self.information = parameters | bidder_types

        self.auction_types = list(parameters["Auction Types"].split(','))
        self.current_auction = self.auction_types[0]

        # Create auctioneer
        reserve_price = parameters["Reserve Price"]
        base_rate = round(random.uniform(0.1, 0.99), 1)
        starting_bid = reserve_price * 1.2

        if self.current_auction == 't2':
            starting_bid = reserve_price * 5

        self.information["Starting Bid"] = starting_bid

        self.auctioneer = Auctioneer(-1, starting_bid, reserve_price, parameters["Auctioneer Type"],
                                     base_rate, self)

        # Create bidders
        self.number_of_bidders = parameters["Number of Bidders"]
        self.bid_schedule = SimultaneousActivation(self)

        self.rounds = 0

        id_bidder = 0

        # For every type, we see how many we have to create
        for bidder_type in bidder_types.keys():
            number_of_bidders_type = int(bidder_types[bidder_type] * self.number_of_bidders / 100)

            # We create the number of bidders for a specific type
            for counter in range(number_of_bidders_type):
                budget = random.randint(reserve_price * 0.6, reserve_price * 6)

                risk = round(random.uniform(0.01, 0.99), 1)
                base_rate = round(random.uniform(0.01, 0.99), 1)
                utility = round(random.uniform(0.01, 0.99), 1)
                bidder_information = (risk, base_rate, utility)

                a = Bidder(id_bidder, budget, bidder_type, bidder_information, self)
                self.bid_schedule.add(a)
                id_bidder = id_bidder + 1

    def step(self):
        """ Simulates an auction or combination of auctions."""

        # First auction type
        self.select_auction_type()

        if len(self.auction_types) == 2:
            # Change the auction type and auctioneer information
            self.current_auction = self.auction_types[1]
            new_base_rate = round(random.uniform(0.01, 0.1), 2)
            self.auctioneer.update_auctioneer(new_base_rate)

            # Second auction type
            self.select_auction_type()

        # Update information
        self.update_metrics()

    def select_auction_type(self):
        """ Determines which auction to be selected. """
        if self.current_auction == 't1' or self.current_auction == 't2':
            self.multi_round_auction()
        elif self.current_auction == 't3' or self.current_auction == 't4':
            self.one_shot_auction(True)

    def multi_round_auction(self):
        """ Simulates an auction with multiple rounds auction."""
        first_round = True
        while True:
            if self.auctioneer.move_next:
                break
            self.one_shot_auction(first_round)
            first_round = False

    def one_shot_auction(self, first_round):
        """ Simulates an auction with only one round."""
        self.rounds = self.rounds + 1
        self.auctioneer.auction()
        self.bid_schedule.step()
        self.auctioneer.decide(first_round)

    def update_metrics(self):
        """Updates the metrics dictionary."""

        if self.auctioneer.winner == -1 or self.auctioneer.winning_bid < self.information['Reserve Price']:
            # No Winner
            self.information['Winner Type'] = 'auctioneer'
            self.information['Revenue'] = self.information['Starting Bid']
            self.information['Winner Satisfaction'] = 0
            self.information['Auctioneer Satisfaction'] = 0
            self.information['Efficiency'] = 0
        else:
            # There is a winner
            winning_bidder = \
                list(filter(lambda bidder: bidder.unique_id == self.auctioneer.winner, self.bid_schedule.agents))
            self.information['Winner Type'] = winning_bidder[0].bidder_type
            self.information['Revenue'] = self.auctioneer.winning_bid

            self.information['Winner Satisfaction'] = (winning_bidder[
                                                           0].budget - self.auctioneer.winning_bid) / self.auctioneer.winning_bid
            self.information['Auctioneer Satisfaction'] = (self.auctioneer.winning_bid - self.information[
                'Reserve Price']) / self.information['Reserve Price']
            self.information['Efficiency'] = abs(
                (self.information['Winner Satisfaction'] - self.information['Auctioneer Satisfaction'])) / self.rounds

        # Extra Metrics
        self.information['Social Welfare'] = self.auctioneer.winning_bid / len(self.bid_schedule.agents)
        self.information['Round No'] = self.rounds
