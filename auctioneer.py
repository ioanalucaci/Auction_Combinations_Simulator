"""
The auctioneer class for the simulation.
"""
from mesa import Agent
import auction_information as info


# TODO: Figure out change_current_bid for all types

class Auctioneer(Agent):
    """Agents that simulates an auctioneer of a certain type."""

    def __init__(self, unique_id, price, reserved_price, auctioneer_type, model):
        """
        Initialisation function for the auctioneer model.

        :param unique_id: the id of the auctioneer
        :param price: the reserved price
        :param auctioneer_type: the type of the auctioneer
        :param model: the auction model it belongs to
        """
        super().__init__(unique_id, model)
        # initial information
        self.price = price
        self.reserved_price = reserved_price
        self.auctioneer_type = auctioneer_type
        self.winner = unique_id
        self.rate = info.auctioneer_type[auctioneer_type][0]

        # initializations
        self.existing_bids = {}
        self.previous_bids = {}
        self.winning_bid = 0
        self.move_next = False
        self.previous_highest_bid = 0
        self.previous_winner = unique_id

    def auction(self):
        """ Simulates an auctioneer's call."""
        if len(self.previous_bids) > 0:
            self.previous_winner = list(self.previous_bids.keys())[0]
            self.previous_highest_bid = self.previous_bids[self.previous_winner]

        if len(self.existing_bids) > 0:
            self.existing_bids = dict(sorted(self.existing_bids.items(), key=lambda item: item[1], reverse=True))
            self.winner = list(self.existing_bids.keys())[0]
            self.winning_bid = self.existing_bids[list(self.existing_bids.keys())[0]]

        self.previous_bids = self.existing_bids
        self.existing_bids = {}

        # print(self.previous_bids)
        # print("The auction price is {0}.".format(str(self.price)))

    def decide(self):
        """ Determines whether to change the current bid or determine the winner."""
        if len(self.existing_bids) == 0:
            self.determine_winner()
        else:
            self.change_current_bid()

    def change_current_bid(self):
        """ Determines how to change the current bid based on the auction type."""
        highest_bid = max(list(self.existing_bids.values()))

        if self.model.current_auction == 't3':
            self.sealedbid_auction()
        if self.model.current_auction == 't4':
            self.vickrey_auction()

        self.update_rate()

        if highest_bid < self.reserved_price:
            self.determine_winner()
        else:
            if self.model.current_auction == 't1':
                self.english_auction(highest_bid)
            elif self.model.current_auction == 't2':
                self.dutch_auction(highest_bid)

    def determine_winner(self):
        """ Determines the winner and how much they have to pay."""
        if len(self.previous_bids) == 0:
            if self.model.current_auction == 't2':
                self.dutch_auction(0)
            return

        # If the auction is the second one, the winner is the highest one.
        if self.model.current_auction == self.model.auction_types[1] and max(
                self.previous_bids.values()) > self.reserved_price:
            self.winner = list(self.previous_bids.keys())[0]
            self.winning_bid = self.previous_bids[self.winner]
        # otherwise, we move forward
        else:
            if self.previous_winner != self.unique_id:
                self.winner = self.previous_winner
                self.winning_bid = self.previous_highest_bid

            self.move_next = True

    def english_auction(self, highest_bid):
        """ Simulates an English auction. We take the highest current bid and add the rate to it."""
        next_highest_bid = highest_bid * (1 + self.rate)
        self.price = next_highest_bid

    def dutch_auction(self, highest_bid):
        """ Simulates a Dutch auction.We take the highest current bid and add the rate to it."""
        if highest_bid == 0:
            self.price = self.price * (1 - self.rate)
        else:
            self.price = max(self.price * (1 - self.rate), highest_bid * 1 + self.rate)

    def sealedbid_auction(self):
        """ Simulates a First Price Sealed Bid auction. Since it is one-shot, we only need the winner."""
        self.existing_bids = dict(sorted(self.existing_bids.items(), key=lambda item: item[1], reverse=True))
        self.winner = list(self.existing_bids.keys())[0]
        self.winning_bid = self.existing_bids[self.winner]

        if self.model.current_auction != self.model.auction_types[1]:
            self.move_next = True

    def vickrey_auction(self):
        """
        Simulates a Vickrey auction. Since it's one-shot, we only need the winner, but the price it'll pay will be
        the second highest bid.
        """

        self.existing_bids = dict(sorted(self.existing_bids.items(), key=lambda item: item[1], reverse=True))
        self.winner = list(self.existing_bids.keys())[0]
        self.winning_bid = self.existing_bids[list(self.existing_bids.keys())[1]]

        if self.model.current_auction != self.model.auction_types[1]:
            self.move_next = True

    def update_auctioneer(self):
        """ Updates the auctioneer after the first round of auctions"""
        self.move_next = False
        self.winner = self.unique_id
        self.rate = info.auctioneer_type[self.auctioneer_type][1]
        self.previous_bids = {}

        # We take the highest bid as the reserved price. This is the most the bidders were willing to pay last auction.
        self.reserved_price = max(self.winning_bid, self.previous_highest_bid)

        if self.model.auction_types[0] == 't2':
            self.price = self.reserved_price * (1 + self.rate)

    def update_rate(self):
        """ Updates the rate based on the auctioneer's profile"""
        self.rate = info.functions[self.auctioneer_type](self.rate, 1, 1)
