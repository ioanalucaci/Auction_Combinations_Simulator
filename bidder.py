"""
The bidder class for the simulation.
"""
from mesa import Agent
import random
import auction_information as info

class Bidder(Agent):
    """Agent that simulates a bidder."""

    def __init__(self, unique_id, budget, bidder_type, bidder_information, model):
        """
        Initialisation function for the bidder agent.

        :param unique_id: the id of the bidder
        :param budget: the bidder's budget
        :param bidder_type: the type of the bidder
        :param model: the auction model it belongs to
        """
        super().__init__(unique_id, model)
        self.budget = budget
        self.bidder_type = bidder_type
        (self.risk, self.rate, self.utility) = bidder_information

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
        """
        Decides if the bidder will bid.

        :param current_bid: the current bid of the auctioneer
        :returns: True if it decides to bid; otherwise False
        """
        # If it's a one-shot, then the bidder has to send a bid
        if self.model.current_auction == 't3' or self.model.current_auction == 't4':
            return True

        if current_bid > self.budget:
            return False

        chance = random.uniform(0, 1)
        if chance < self.risk:
            return True
        else:
            return False

    def counter_proposal(self, current_bid):
        """
        Decides how much to bid.

        :param current_bid: The current bid of the auctioneer.
        """
        personal_bid = 0
        self.rate = info.functions[self.bidder_type](self.rate, self.utility, self.risk)

        if self.model.current_auction == 't1':
            personal_bid = self.english_auction(current_bid)
        elif self.model.current_auction == 't2':
            personal_bid = self.dutch_auction(current_bid)
        elif self.model.current_auction == 't3':
            personal_bid = self.sealedbid_auction(current_bid)
        elif self.model.current_auction == 't4':
            personal_bid = self.vickrey_auction(current_bid)

        if personal_bid > 0:
            self.model.auctioneer.existing_bids[self.unique_id] = personal_bid

    def english_auction(self, current_bid):
        """
        Simulates an English auction.

        :param current_bid: The current bid of the auctioneer.
        :return: the personal bid to submit.
        """

        personal_bid = current_bid + current_bid * self.rate

        if personal_bid > self.budget:
            return -10

        return personal_bid

    def dutch_auction(self, current_bid):
        """
        Simulates a Dutch auction.

        :param current_bid: The current bid of the auctioneer.
        :return: the personal bid to submit.
        """

        personal_bid = current_bid - current_bid * self.rate

        if personal_bid > self.budget:
            personal_bid = self.budget

        return personal_bid

    # TODO: Figure these two out
    def sealedbid_auction(self, current_bid):
        """
        Simulates a first-price sealed-bid auction.

        :param current_bid: The current bid of the auctioneer.
        :return: the personal bid to submit.
        """
        pass

    def vickrey_auction(self, current_bid):
        """
        Simulates a Vickrey auction.

        :param current_bid: The current bid of the auctioneer.
        :return: the personal bid to submit.
        """
        pass
