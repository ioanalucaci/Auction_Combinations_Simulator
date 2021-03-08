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

    def __init__(self, unique_id, price, reserved_price, auctioneer_type, model):
        """
        Initialisation function for the auctioneer model.

        :param unique_id: the id of the auctioneer
        :param price: the reserved price
        :param auctioneer_type: the type of the auctioneer
        :param model: the auction model it belongs to
        """
        super().__init__(unique_id, model)
        self.price = price
        self.reserved_price = reserved_price
        self.auctioneer_type = auctioneer_type
        self.existing_bids = {}
        self.previous_bids = {}
        self.winner = unique_id
        self.rate = info.auctioneer_type[auctioneer_type]
        self.winning_bid = 0
        self.bidders_for_next_round = []
        self.move_next = False

    def auction(self):
        """ Simulates an auctioneer's call."""
        self.previous_bids = self.existing_bids
        self.existing_bids = {}
        print(self.previous_bids)
        print("The auction price is {0}.".format(str(self.price)))

    def decide(self):
        """ Determines whether to change the current bid or determine the winner."""
        if len(self.existing_bids) == 0:
            self.determine_winner()
        else:
            self.change_current_bid()


    def change_current_bid(self):
        """ Determines how to change the current bid based on the auction type."""
        highest_bid = max(list(self.existing_bids.values()))
        if highest_bid < self.reserved_price:
            self.determine_winner()
        else:
            if self.model.current_auction == 't1':
                self.english_auction(highest_bid)
            elif self.model.current_auction == 't2':
                self.dutch_auction(highest_bid)

    def determine_winner(self):
        """ Determines the winner and how much they have to pay."""
        # We order first based on price descending
        self.previous_bids = dict(sorted(self.previous_bids.items(), key=lambda item: item[1], reverse=True))
        print(self.previous_bids.values())

        # If the auction is the second one, the winner is the highest one.
        if self.model.current_auction == self.model.auction_types[1] and max(self.previous_bids.values()) > self.reserved_price:
            self.winner = list(self.previous_bids.keys())[0]
            self.winning_bid = self.previous_bids[self.winner]

        # We can select here the bidders to go in the next round;
        # for now, bidders who bid no less than 10% lower than the highest bid
        else:
            for bidder in self.previous_bids.keys():
                if self.previous_bids[bidder] >= self.winning_bid * 1.1:
                    self.bidders_for_next_round.append(bidder)
                else:
                    break
            self.move_next = True

    def english_auction(self, highest_bid):
        """ Simulates an English auction. We take the highest current bid and add the rate to it."""
        next_highest_bid = highest_bid * (100 + self.rate)/100
        if self.price == highest_bid:
            self.price = next_highest_bid*(100 + self.rate)/100
        elif self.price > highest_bid:
            self.price = self.price * (100 + self.rate) / 100
        else:
            self.price = next_highest_bid

    def dutch_auction(self, highest_bid):
        """ Simulates a Dutch auction.We take the highest current bid and add the rate to it."""
        self.price = highest_bid * (100 + self.rate)/100