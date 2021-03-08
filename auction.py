"""
The auction class for the simulation.
"""
import random
from mesa import Model
from mesa.time import SimultaneousActivation
from bidder import Bidder
from auctioneer import Auctioneer


# TODO: figure out how to pass information between auctions
# TODO: Figure out how to make the dutch and english auction

class Auction(Model):
    """Model that simulates an auction situation. Used to dictate the communication between auctioneers and bidders."""

    def __init__(self, number_of_bidders, auction_types, starting_price, reserved_price, auctioneer_type, bidder_types):
        """
        Initialisation function for the auction model.

        :param number_of_bidders: the number of bidders that take part in this auction
        :param auction_types: the types of auction to be combined
        :param reserved_price: the reserved price at which the auction will start
        :param auctioneer_type: the auctioneer type that will be used for this auction
        :param bidder_types: the types of bidders to join this auction alongside their percentage
        """

        self.auction_types = auction_types
        self.current_auction = auction_types[0]

        # Create auctioneer
        self.auctioneer = Auctioneer(-3, starting_price, reserved_price, auctioneer_type, self)

        # Create bidders
        self.number_of_bidders = number_of_bidders
        self.bid_schedule = SimultaneousActivation(self)

        id_bidder = 0

        # For every type, we see how many we have to create
        for bidder_type in bidder_types.keys():
            number_of_bidders_type = int(bidder_types[bidder_type] * self.number_of_bidders / 100)

            # We create the number of bidders for a specific type
            for counter in range(number_of_bidders_type):
                budget = random.randint(reserved_price * 0.6, reserved_price * 1.4)
                a = Bidder(id_bidder, budget, bidder_type, self)
                self.bid_schedule.add(a)
                id_bidder = id_bidder + 1

    def step(self):
        """ Simulates an auction or combination of auctions."""

        # First auction type
        self.select_auction_type()

        self.current_auction = self.auction_types[1]

        # We remove all the agents that did not move forward
        for bidder in self.bid_schedule.agents:
            if bidder.unique_id not in self.auctioneer.bidders_for_next_round:
                self.bid_schedule.agents.remove(bidder)
        self.auctioneer.bidders_for_next_round = []
        self.auctioneer.move_next = False

        # Then the second auction type
        self.select_auction_type()

        # Announce the winner
        print("Bidder {0} won with price {1}".format(self.auctioneer.winner, self.auctioneer.winning_bid))

    def select_auction_type(self):
        """ Determines which auction to be selected. """
        if self.current_auction == 't1' or self.current_auction == 't2':
            self.multi_round_auction()
        elif self.current_auction == 't3' or self.current_auction == 't4':
            self.one_shot_auction()

    # TODO: Skeleton structures for now

    def multi_round_auction(self):
        """ Simulates an auction with multiple rounds auction."""
        while True:
            if self.auctioneer.winner != self.auctioneer.unique_id or self.auctioneer.move_next:
                break
            self.auctioneer.auction()
            self.bid_schedule.step()
            self.auctioneer.decide()

    def one_shot_auction(self):
        """ Simulates an auction with only one round."""
        pass
