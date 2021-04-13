"""
The functions used by the bidder and auctioneer types that can be changed at any point.
"""
import math


def update_rate(profile, old_rate, utility, risk):
    functions = {
        'A': lambda rate, utility, risk: rate,
        'B': lambda rate, utility, risk: rate * risk + utility,
        'C': lambda rate, utility, risk: utility - rate * risk,
        'D': lambda rate, utility, risk: math.sin(rate) + (utility + risk) * rate
    }

    new_rate = functions[profile](old_rate, utility, risk)

    while new_rate > 0.3:
        difference = new_rate - old_rate

        difference = difference / 100

        new_rate = old_rate + difference

    if new_rate <= 0:
        new_rate = old_rate - old_rate / 1000

    return round(new_rate, 2)
