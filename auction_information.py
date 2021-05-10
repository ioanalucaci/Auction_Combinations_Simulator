"""
The functions used by the bidder and auctioneer types that can be changed at any point.
"""
import math


def update_rate(profile, old_rate, utility, risk):
    """
    Updates the rate of the agent.

    :param profile: the agent's profile.
    :param old_rate: the previous rate
    :param utility: the utility
    :param risk: the risk
    :return: the new rate
    """
    functions = {
        'A': lambda rate, utility, risk: rate,
        'B': lambda rate, utility, risk: rate * risk + utility,
        'C': lambda rate, utility, risk: utility - rate * risk,
        'D': lambda rate, utility, risk: math.sin(rate) + (utility + risk)
    }

    new_rate = functions[profile](old_rate, utility, risk)

    # We ensure rate can only be between 0 and 0.1
    while new_rate > 0.1:
        difference = (new_rate - old_rate) / 100

        new_rate = old_rate + difference

    while new_rate <= 0:
        difference = old_rate / 100

        new_rate = old_rate - difference

    return new_rate
