import csv
from datetime import datetime


def write_metrics(list_of_auctions):
    """
    Writes the metrics in a csv file

    :param file_name: the name of the file to write the metrics in.
    :param list_of_auctions: the list of auctions to be exported in the csv file
    :return:
    """
    today = datetime.today()

    file_name = "metrics " + today.strftime('%d-%m-%y') + ".csv"

    with open(file_name, mode='w+') as metrics_file:
        metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # These are the table headers.
        metrics_writer.writerow(
            ['Auction Types', 'Auctioneer Type', 'Bidder a %', 'Bidder b %', 'Bidder c %', 'Bidder d %', 'Winner Type',
             'Starting Bid', 'Winning Bid', '# Rounds'])

        # These are the headers they correspond to in terms of how the auction is coded.
        headers = ('Auction Types', 'Auctioneer Type', 'a', 'b', 'c', 'd', 'Winner Type', 'Starting Bid', 'Winning Bid',
                   'Round No')

        for auction in list_of_auctions:
            to_be_published = []

            for header in headers:
                to_be_published.append(auction.information[header])

            metrics_writer.writerow(to_be_published)
