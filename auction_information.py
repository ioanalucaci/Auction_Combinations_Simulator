"""
The information about the bidder and auctioneer types that can be changed at any point.
"""
import math

# Bidder types of the shape (risk, base_rate, utility)
bidders_type = {
    'A': (0.001, 0.01, 0.01),
    'B': (0.01, 0.01, 0.02),
    'C': (0.05, 0.02, 0.03),
    'D': (0.02, 0.02, 0.04)
}

# Auctioneer types of the shape (first_rate, second_rate)
auctioneer_type = {
    'A': (0.02, 0.001),
    'B': (0.05, 0.005),
    'C': (0.02, 0.01),
    'D': (0.01, 0.01)
}

functions = {
    'A': lambda rate, utility, risk: rate,
    'B': lambda rate, utility, risk: 1 - 2 ** (- rate / (utility + risk)),
    'C': lambda rate, utility, risk: 2 ** (- rate / (utility + risk)),
    'D': lambda rate, utility, risk: math.sin(rate) + (utility + risk) * rate
   # 'd': lambda rate, utility, risk: math.fabs(math.cos(utility / (rate * risk))),
}

# 'b': lambda rate, utility, risk: 1 - math.exp(- rate * (2 - utility - risk)),
# 'c': lambda rate, utility, risk: math.fabs(math.exp(rate * (utility + risk - 2) - 1)),
# 'd': lambda rate, utility, risk: math.sin(rate) + (utility + risk) * rate
