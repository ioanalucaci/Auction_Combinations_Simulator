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

    def __init__(self, parameters, bidder_types, agents_factory):
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
        auct_info = agents_factory.auctioneer

        self.information["Starting Bid"] = auct_info["starting_bid"]

        self.auctioneer = Auctioneer(-1, auct_info["starting_bid"], auct_info["reserve_price"], parameters["Auctioneer Type"],
                                     auct_info["base_rate"], self)

        # Create bidders
        self.bid_schedule = SimultaneousActivation(self)

        self.rounds = 0

        bidders_info = agents_factory.bidders
        for counter in range(0, len(bidders_info)):
            bidder_info = bidders_info[counter]
            bidder = Bidder(counter, bidder_info["budget"], bidder_info["bidder_type"], bidder_info["bidder_information"], self)
            self.bid_schedule.add(bidder)

    def step(self):
        """ Simulates an auction or combination of auctions."""
        # First auction type
        #print("start")
        #print(self.current_auction)
        self.select_auction_type()

        if len(self.auction_types) == 2:
            # Change the auction type and auctioneer information
            self.current_auction = self.auction_types[1]
            new_base_rate = round(random.uniform(0.01, 0.05), 2)
            self.auctioneer.update_auctioneer(new_base_rate)

            #print(self.current_auction)

            # Second auction type
            self.select_auction_type()
        #print(self.auctioneer.winning_bid)
        #print("----------------")
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
            self.information['Revenue'] = - self.information['Reserve Price']
            self.information['Winner Satisfaction'] = 0
            self.information['Auctioneer Satisfaction'] = -1
            self.information['Efficiency'] = 0
        else:
            # There is a winner
            winning_bidder = \
                list(filter(lambda bidder: bidder.unique_id == self.auctioneer.winner, self.bid_schedule.agents))
            self.information['Winner Type'] = winning_bidder[0].bidder_type
            self.information['Revenue'] = self.auctioneer.winning_bid - self.information["Reserve Price"]

            self.information['Winner Satisfaction'] = (winning_bidder[
                                                           0].budget - self.auctioneer.winning_bid) / self.auctioneer.winning_bid
            self.information['Auctioneer Satisfaction'] = (self.auctioneer.winning_bid - self.information[
                'Reserve Price']) / self.information['Reserve Price']
            self.information['Efficiency'] = abs(
                (self.information['Winner Satisfaction'] - self.information['Auctioneer Satisfaction'])) / self.rounds

        # Extra Metrics
        self.information['Social Welfare'] = self.information['Revenue'] / len(self.bid_schedule.agents)
        self.information['Round No'] = self.rounds
