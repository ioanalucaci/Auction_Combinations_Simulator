"""
The functions used by the bidder and auctioneer types that can be changed at any point.
"""
import math

functions = {
    'A': lambda rate, utility, risk: rate,
    'B': lambda rate, utility, risk: 1 - 2 ** (- rate / (utility + risk)),
    'C': lambda rate, utility, risk: 2 ** (- rate / (utility + risk)),
    'D': lambda rate, utility, risk: math.sin(rate) + (utility + risk) * rate
}
