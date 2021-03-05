"""
The information about the bidder and auctioneer types that can be changed at any point.
"""

# Bidder types
bidders_type = {
    'b1': [("risk", 2), ("utility", 2)],
    'b2': [("risk", 10), ("utility", 10)],
    'b3': [("risk", 20), ("utility", 20)],
    'b4': [("risk", 2), ("utility", 20)],
    'b5': [("risk", 20), ("utility", 2)]
}

# Auctioneer types
auctioneer_type = {
    'a1': 2,
    'a2': 10,
    'a3': 20,
}
