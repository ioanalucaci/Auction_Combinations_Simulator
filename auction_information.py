"""
The information about the bidder and auctioneer types that can be changed at any point.
"""
import math

# TODO: implement functions to return a number within certain limits which will always be constant
#   (for constant), always be lower(for descending) etc.

# Bidder types of the shape (risk, base_rate, utility)
bidders_type = {
    'constant': (0.2, 0.02, 0.1),
    'ascending': (0.1, 0.1, 0.1),
    'descending': (0.2, 0.2, 0.1),
    'non-monotonic': (0.02, 0.2, 0.1)
}

# Auctioneer types of the shape (first_rate, second_rate)
auctioneer_type = {
    'constant': (0.02, 0.01),
    'ascending': (0.1, 0.05),
    'descending': (0.2, 0.1),
    'non-monotonic': (0.3, 0.1)
}

functions = {
    'constant': lambda rate, utility, risk: rate,
    'ascending': lambda rate, utility, risk: 1 - math.exp(- rate * (2 - utility - risk)),
    'descending': lambda rate, utility, risk: math.fabs(math.exp(rate * (utility + risk - 2) - 1)),
    'non-monotonic': lambda rate, utility, risk: math.sin(rate) + (utility + risk) * rate,
}
