import csv
from datetime import datetime


def write_metrics(headers):
    """
    Writes the metrics in a csv file

    :param headers: the headers for the csv file.
    :return the name of the .csv file
    """
    today = datetime.today()

    file_name = "metrics " + today.strftime('%d-%m-%y') + ".csv"

    with open(file_name, mode='w+') as metrics_file:
        metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # First, write the table header.
        metrics_writer.writerow(headers)
    return file_name


def write_simulators(file_name, list_of_auctions, headers):
    """
    Writes the simulators information in a csv file

    :param headers: The headers for the csv file.
    :param file_name: the name of the file.
    :param list_of_auctions: the list of auctions to be exported in the csv file
    """
    with open(file_name, mode='a') as metrics_file:
        metrics_writer = csv.writer(metrics_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Then, for each auction, extract the information
        for auction in list_of_auctions:
            to_be_published = []
            for header in headers:
                to_be_published.append(auction.information[header])
            metrics_writer.writerow(to_be_published)
