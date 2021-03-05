"""
The bidder class for the simulation.
"""
from mesa import Agent
import auction_information


# TODO: Figure out decision_to_bid
# TODO: figure out counter_proposal for the different types of auction

class Bidder(Agent):
    """Agent that simulates a bidder."""

    def __init__(self, unique_id, budget, bidder_type, model):
        """
        Initialisation function for the bidder agent.

        :param unique_id: the id of the bidder
        :param budget: the bidder's budget
        :param bidder_type: the type of the bidder
        :param model: the auction model it belongs to
        """
        super().__init__(unique_id, model)
        self.budget = budget
        self.type = bidder_type

    def step(self):
        """ Takes a step in an auction."""

        current_bid = self.model.auctioneer.price
        if self.decision_to_bid(current_bid):
            self.counter_proposal(current_bid)

    def advance(self):
        """ Advances the bidder through the model."""
        if self.model.auctioneer.winner == self.unique_id:
            print("Bidder {0} is happy! Won with price {1}".format(self.unique_id, self.budget))

    def decision_to_bid(self, current_bid):
        """ Decides if the bidder will bid."""
        return True

    def counter_proposal(self, current_bid):
        """ Decides how much to bid."""
        self.model.auctioneer.existing_bids[
            self.unique_id] = self.budget  # counter proposal should be a function that takes as parameter the profile selection and any other parameters that we might need
        return True

    # TODO: Skeleton for now
    def english_auction(self):
        """ Simulates an English auction."""
        return True

    def dutch_auction(self):
        """ Simulates a Dutch auction."""
        return True

    def sealedbid_auction(self):
        """ Simulates a first-price sealed-bid auction."""
        return True

    def vickrey_auction(self):
        """ Simulates a Vickrey auction."""
        return True
