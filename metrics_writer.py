import csv
import mesa
import bidder
import auctioneer


def write_metrics(file_name, list_of_auctions):
    """
    Writes the metrics in a csv file

    :param file_name: the name of the file to write the metrics in.
    :param list_of_auctions: the list of auctions to be exported in the csv file
    :return:
    """

    with open(file_name, mode='w') as metrics_file:
        metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        metrics_writer.writerow(
            ['Auction Types', 'Auctioneer Type', 'Bidder a %', 'Bidder b %', 'Bidder c %', 'Bidder d %', 'Winner Type',
             'Starting Bid', 'Winning Bid', 'Round No'])

        headers = ('Auction Types', 'Auctioneer Type', 'a', 'b', 'c', 'd', 'Winner Type', 'Starting Bid', 'Winning Bid',
                   'Round No')
        for auction in list_of_auctions:
            to_be_published = []

            for header in headers:
                to_be_published.append(auction.information[header])

            metrics_writer.writerow(to_be_published)
