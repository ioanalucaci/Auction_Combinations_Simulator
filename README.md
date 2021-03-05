# Final Project

This is the code section for my final project.

### Notation meanings:

###### Auction
There are 4 types of auctions that can be combined:
- T1 - English
- T2 - Dutch
- T3 - First-price sealed-bid
- T4 - Vickrey

###### Auctioneer
The auctioneer varies in terms of how much the auction price will be changed between rounds (when applicable). Thus, there will be three profiles:
- A1 - Slow auctioneer - will try to sell the item by changing the price by a very small amount each round
- A2 - Neutral auctioneer - will sell the item by changing the price by a normal amount each round
- A3 - Fast auctioneer - will try to sell the item by changing the price by a very big amount each round

###### Bidder
The bidder varies in terms of two parameters: risk and utility. Risk refers to how likely is it for the bidder to place a bid. Utility refers to how valued is the item to be sold to the specific bidder. Thus, there are five profiles:
- B1 - Low risk, low utility
- B2 - Medium risk, medium utility
- B3 - High risk, high utility
- B4 - Low risk, high utility
- B5 - high risk, low utility
