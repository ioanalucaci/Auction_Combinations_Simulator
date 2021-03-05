"""
The information about the bidder and auctioneer types that can be changed at any point.
"""

# Bidder types of the shape (risk, utility)
bidders_type = {
    'b1': (2, 0.2),
    'b2': (10, 1),
    'b3': (20, 2),
    'b4': (2, 2),
    'b5': (20, 0.2)
}

# Auctioneer types of the shape price_change
auctioneer_type = {
    'a1': 2,
    'a2': 10,
    'a3': 20,
}
