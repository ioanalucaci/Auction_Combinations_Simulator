"""
The auctioneer class for the simulation.
"""
from mesa import Agent
import auction_information as info


class Auctioneer(Agent):
    """Agents that simulates an auctioneer of a certain type."""

    def __init__(self, unique_id, price, reserved_price, auctioneer_type, base_rate, model):
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
            if self.price < max(self.existing_bids.values()) or self.model.current_auction == 't2':
                self.winner = list(self.existing_bids.keys())[0]
                self.winning_bid = self.existing_bids[list(self.existing_bids.keys())[0]]

        self.previous_bids = self.existing_bids
        self.existing_bids = {}

        # print("-------------------------------")
        # print(self.previous_bids)
        # print("The auction price is {0}.".format(str(self.price)))
        # print("Highest bid is {0} with oldest highest bid being {1}".format(self.winning_bid, self.previous_highest_bid))

    def decide(self, first_round):
        """ Determines whether to change the current bid or determine the winner."""
        # print(self.existing_bids)
        # print("--------------------------------")

        if len(self.existing_bids) == 0 and not first_round:
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
        if self.model.current_auction == 't3':
            self.sealedbid_auction()
        if self.model.current_auction == 't4':
            self.vickrey_auction()

        info.update_rate(self.auctioneer_type, self.rate, 1, 1)

        # The Dutch has a special case where the price can decrease with no bidders
        if highest_bid < self.reserved_price:
            if self.model.current_auction == 't2':
                self.dutch_auction(highest_bid)
            else:
                self.determine_winner()
        else:
            if self.model.current_auction == 't1':
                self.english_auction(highest_bid)
            elif self.model.current_auction == 't2':
                self.dutch_auction(highest_bid)

    def determine_winner(self):
        """ Determines the winner and how much they have to pay."""

        # There are times where there are no bids and we only have to run the Dutch auction again
        if self.model.current_auction == 't2' and len(self.previous_bids) == len(self.existing_bids) == 0:
            self.dutch_auction(0)
        else:
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

        if self.model.auction_types[0] == 't2':
            self.price = self.reserved_price * (1 + self.rate)

        if self.model.auction_types[-1] == 't2':
            self.reserved_price = max(self.winning_bid, self.previous_highest_bid)
            self.price = self.price * (1 - self.rate)

        if self.model.auction_types[0] in ['t3', 't4']:
            self.price = self.reserved_price

        self.winner = self.unique_id
        self.winning_bid = 0
        self.previous_highest_bid = 0
        self.previous_winner = self.unique_id
