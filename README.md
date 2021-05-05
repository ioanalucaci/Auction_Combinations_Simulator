# Final Project

This is the code section for my final project.

## Notation meanings:

### Auction
There are 4 types of auctions that can be combined:
- E - English
- D - Dutch
- F - First-price sealed-bid
- V - Vickrey

### Auctioneer
The auctioneer has, at the moment, two rates: the first auction rate, and the second auction rate. 
This can be seen in *agents_factory.py*

### Bidder
The bidder has three parameters:
- **risk** - value between 0 and 1
- **utility** - value between 0 and 1
- **base rate** - value between 0 and 0.1

These parameters are randomly constructed in *agents_factory.py*

### Functions
There are 4 functions connected to 4 profiles at the moment:
- *A* : constant function
- *B* : increasing function
- *C* : decreasing function
- *D* : non-monotonous function

These functions can be changed in *auction_information.py*