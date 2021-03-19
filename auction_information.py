"""
The information about the bidder and auctioneer types that can be changed at any point.
"""
import math

# Bidder types of the shape (risk, base_rate, utility)
bidders_type = {
    'a': (0.5, 0.1, 0.1),
    'b': (0.5, 0.1, 0.1),
    'c': (0.5, 0.2, 0.1),
    'd': (0.5, 0.2, 0.1)
}

# Auctioneer types of the shape (first_rate, second_rate)
auctioneer_type = {
    'a': (0.2, 0.01),
    'b': (0.5, 0.05),
    'c': (0.2, 0.1),
    'd': (0.5, 0.1)
}

# TODO: As long as they're different and they capture real-life aspects, and have a different shape
functions = {
    'a': lambda rate, utility, risk: rate,
    'b': lambda rate, utility, risk: 1 - math.exp(- rate * (2 - utility - risk)),
    'c': lambda rate, utility, risk: math.fabs(math.exp(rate * (utility + risk - 2) - 1)),
    'd': lambda rate, utility, risk: math.sin(rate) + (utility + risk) * rate,
}
