"""
The auctioneer class for the simulation.
"""
import random
from mesa import Agent
import auction_information as info


class Auctioneer(Agent):
    """Agents that simulates an auctioneer of a certain type."""

    def __init__(self, unique_id, price, reserved_price, auctioneer_type, base_rate, model):
        """
        Initialisation function for the auctioneer model.

        :param unique_id: the id of the auctioneer
        :param price: the starting price price
        :param reserved_price: the reserved price
        :param auctioneer_type: the type of the auctioneer
        :param base_rate: the starting rate
        :param model: the auction model it belongs to
        """
        super().__init__(unique_id, model)
        # initial information
        self.price = price
        self.reserved_price = reserved_price
        self.auctioneer_type = auctioneer_type
        self.winner = unique_id
        self.rate = base_rate

        # initializations
        self.existing_bids = {}
        self.previous_bids = {}
        self.winning_bid = 0
        self.move_next = False
        self.previous_highest_bid = 0
        self.previous_winner = unique_id

    def auction(self):
        """ Simulates an auctioneer's call."""

        # We keep track of the previous highest bid
        if self.previous_highest_bid < self.winning_bid:
            self.previous_winner = self.winner
            self.previous_highest_bid = self.winning_bid

        # And we keep track of the current highest bid
        if len(self.existing_bids) > 0:
            self.existing_bids = dict(sorted(self.existing_bids.items(), key=lambda item: item[1], reverse=True))

            # We update the current 'winner' only if it's higher than the current price or we're in a Dutch auction
            if self.price < max(self.existing_bids.values()) or self.model.current_auction == 'D':
                self.winner = list(self.existing_bids.keys())[0]
                self.winning_bid = self.existing_bids[list(self.existing_bids.keys())[0]]

        self.previous_bids = self.existing_bids
        self.existing_bids = {}

    def decide(self, first_round):
        """ Determines whether to change the current bid or determine the winner."""
        if len(self.existing_bids) == 0 and not first_round and self.model.current_auction != 'D':
            self.determine_winner()
        else:
            self.change_current_bid()

    def change_current_bid(self):
        """ Determines how to change the current bid based on the auction type."""

        self.existing_bids = dict(sorted(self.existing_bids.items(), key=lambda item: item[1], reverse=True))
        highest_bid = self.existing_bids[list(self.existing_bids.keys())[0]] if len(self.existing_bids) > 0 else 0

        # If the current winning bid is smaller than the highest bid, we update accordingly
        if self.winning_bid < highest_bid:
            self.previous_winner = self.winner
            self.previous_highest_bid = self.winning_bid
            self.winner = list(self.existing_bids.keys())[0]
            self.winning_bid = highest_bid

        # After that, we choose which function is best for the auction type
        if self.model.current_auction == 'F':
            self.sealedbid_auction()
        if self.model.current_auction == 'V':
            self.vickrey_auction()

        self.rate = info.update_rate(self.auctioneer_type, self.rate, 1, 1)

        # The Dutch has a special case where the price can decrease with no bidders
        if highest_bid < self.reserved_price:
            if self.model.current_auction == 'D':
                self.dutch_auction(highest_bid)
            else:
                self.determine_winner()
        else:
            if self.model.current_auction == 'E':
                self.english_auction(highest_bid)
            elif self.model.current_auction == 'D':
                self.dutch_auction(highest_bid)

    def determine_winner(self):
        """ Determines the winner and how much they have to pay."""
        previous_bids_max = max(self.previous_bids.values()) if len(self.previous_bids) > 0 else 0

        if self.reserved_price < previous_bids_max and self.winning_bid < previous_bids_max:
            self.winner = list(self.previous_bids.keys())[0]
            self.winning_bid = self.previous_bids[self.winner]
        elif self.previous_winner != self.unique_id and self.winning_bid < self.previous_highest_bid:
            self.winner = self.previous_winner
            self.winning_bid = self.previous_highest_bid

        self.move_next = True

    def english_auction(self, highest_bid):
        """ Simulates an English auction. We take the highest current bid and add the rate to it."""
        next_highest_bid = highest_bid * (1 + self.rate)
        self.price = next_highest_bid

    def dutch_auction(self, highest_bid):
        """ Simulates a Dutch auction.We take the highest current bid and add the rate to it."""
        price = max(self.price * (1 - self.rate), highest_bid * (1 + self.rate))

        # If we reached below the reserved price, we exit
        if self.reserved_price > price:
            self.move_next = True
        # If we're in the risk of raising the price or going below what the winning bid currently is, determine winner
        elif self.price < price or price < self.winning_bid:
            self.determine_winner()
        else:
            self.price = price

    def sealedbid_auction(self):
        """ Simulates a First Price Sealed Bid auction. Since it is one-shot, we only need the winner."""
        self.existing_bids = dict(sorted(self.existing_bids.items(), key=lambda item: item[1], reverse=True))
        self.winner = list(self.existing_bids.keys())[0]
        self.winning_bid = self.existing_bids[self.winner]

        if self.model.current_auction != self.model.auction_types[-1]:
            self.move_next = True

    def vickrey_auction(self):
        """
        Simulates a Vickrey auction. Since it's one-shot, we only need the winner, but the price it'll pay will be
        the second highest bid.
        """
        self.existing_bids = dict(sorted(self.existing_bids.items(), key=lambda item: item[1], reverse=True))
        self.winner = list(self.existing_bids.keys())[0]

        if len(self.existing_bids) >= 2:
            self.winning_bid = self.existing_bids[list(self.existing_bids.keys())[1]]
        else:
            self.winning_bid = self.existing_bids[list(self.existing_bids.keys())[0]]

        if self.model.current_auction != self.model.auction_types[-1]:
            self.move_next = True

    def update_auctioneer(self, new_base_rate):
        """ Updates the auctioneer after the first round of auctions"""
        self.move_next = False
        self.rate = new_base_rate
        self.previous_bids = {}

        # We take the highest bid as the reserved price. This is the most the bidders were willing to pay last auction.
        self.reserved_price = max(self.winning_bid, self.previous_highest_bid, self.price)

        if self.model.auction_types[0] == 'D':
            self.price = self.reserved_price * (1 + self.rate)

        if self.model.auction_types[0] in ['F', 'V']:
            self.price = self.reserved_price

        if self.model.auction_types[-1] == 'D':
            self.reserved_price = max(self.winning_bid, self.previous_highest_bid)
            multiplier = round(random.uniform(1.3, 2), 1)
            self.price = self.reserved_price * multiplier
