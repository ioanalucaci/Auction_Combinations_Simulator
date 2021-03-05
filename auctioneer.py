"""
The auctioneer class for the simulation.
"""
from mesa import Agent
import auction_information as info


# TODO: Figure out the decision for the different auctions
# TODO: Figure out change_current_bid for all types
# TODO: Figure out how to determine the winner for all types AND how much to charge them

class Auctioneer(Agent):
    """Agents that simulates an auctioneer of a certain type."""

    def __init__(self, unique_id, price, auctioneer_type, model):
        """
        Initialisation function for the auctioneer model.

        :param unique_id: the id of the auctioneer
        :param price: the reserved price
        :param auctioneer_type: the type of the auctioneer
        :param model: the auction model it belongs to
        """
        super().__init__(unique_id, model)
        self.price = price
        self.auctioneer_type = auctioneer_type
        self.existing_bids = {}
        self.winner = unique_id
        self.rate = info.auctioneer_type[auctioneer_type]
        self.winning_bid = 0

    def auction(self):
        """ Simulates an auctioneer's call."""
        print("The auction price is {0}.".format(str(self.price)))

    def decide(self):
        """ Determines whether to change the current bid or determine the winner."""
        if len(self.existing_bids) == 0:
            self.change_current_bid()
        else:
            self.determine_winner()

    def change_current_bid(self):
        """ Determines how to change the current bid based on the auction type."""
        return True

    def determine_winner(self):
        """ Determines the winner and how much they have to pay."""
        return True

    # TODO: Skeleton structures for now
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