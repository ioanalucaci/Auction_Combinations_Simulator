from mesa import Model
from mesa.time import SimultaneousActivation
from bidder import Bidder
from auctioneer import Auctioneer

class MoneyModel(Model):
    """Model with some number of agents. Each model will contain multiple agents."""

    def __init__(self, N):
        self.num_agents = N

        self.bid_schedule = SimultaneousActivation(self)
        # Create agents
        self.auctioneer = Auctioneer(-3, self)
        for i in range(self.num_agents):
            a = Bidder(i, self)
            self.bid_schedule.add(a)

    def step(self):
        """Advance the model by one step."""
        self.auctioneer.auction()
        self.bid_schedule.step()
        self.auctioneer.choose()
