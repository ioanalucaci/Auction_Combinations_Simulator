import random
import matplotlib.pyplot as plt
import pandas as pd


def visualise_data(agent_type, data_type, file_name):
    """
    Analyses the data in terms of ANOVA test, while also presenting a histogram and bell curve for the results.

    :param agent_type: Whether we analyse the bidder or the auctioneer type.
    :param data_type: What we analyse, i.e. winner bid, ROI etc.
    :param file_name: The name of the file where the data is stored.
    """

    # Visualisation
    data_for_frame = {}
    size = 10

    csv_data = extract_information(file_name, agent_type, data_type)

    for element in ['A', 'B', 'C', 'D']:
        if len(csv_data[element]) > size:
            data_for_frame[element] = random.sample(csv_data[element], size)

    data_to_plot = pd.DataFrame(data_for_frame)

    # Shows a histogram
    data_to_plot.plot.hist()

    # Shows a Bell Curve
    data_to_plot.plot.kde()

    plt.show()


def extract_information(file_name, agent_type, data_type):
    """
    Extract the required information from the CSV file.

    :param file_name: The name of the CSV file.
    :param agent_type: whether we're looking at the auctioneer or winner
    :param data_type: what column we're focusing on
    :return:
    """
    metrics_data = pd.read_csv(file_name)

    # Separating the data based on the winner type and extracting only what's important
    csv_data = {
        'A': list(metrics_data[data_type][metrics_data[agent_type] == 'A']),
        'B': list(metrics_data[data_type][metrics_data[agent_type] == 'B']),
        'C': list(metrics_data[data_type][metrics_data[agent_type] == 'C']),
        'D': list(metrics_data[data_type][metrics_data[agent_type] == 'D'])
    }

    return csv_data
