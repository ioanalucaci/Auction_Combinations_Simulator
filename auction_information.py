"""
The information about the bidder and auctioneer types that can be changed at any point.
"""
import math

# Bidder types of the shape (risk, base_rate, utility)
bidders_type = {
    'a': (0.001, 0.01, 0.01),
    'b': (0.01, 0.01, 0.02),
    'c': (0.05, 0.02, 0.03),
    'd': (0.02, 0.02, 0.04)
}

# Auctioneer types of the shape (first_rate, second_rate)
auctioneer_type = {
    'a': (0.02, 0.001),
    'b': (0.05, 0.005),
    'c': (0.02, 0.01),
    'd': (0.01, 0.01)
}

# TODO: As long as they're different and they capture real-life aspects, and have a different shape
functions = {
    'a': lambda rate, utility, risk: rate,
    'b': lambda rate, utility, risk: 1 - math.exp(- rate * (2 - utility - risk)),
    'c': lambda rate, utility, risk: math.fabs(math.exp(rate * (utility + risk - 2) - 1)),
    'd': lambda rate, utility, risk: math.sin(rate) + (utility + risk) * rate,
}
