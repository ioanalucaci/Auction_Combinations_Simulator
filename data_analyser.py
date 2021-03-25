import pandas as pd
import random
import matplotlib.pyplot as plt
from scipy import stats


def visualise_data(agent_type, data_type, file_name):
    """
    Analyses the data in terms of ANOVA test, while also presenting a histogram and bell curve for the results.

    :param agent_type: Whether we analyse the bidder or the auctioneer type.
    :param data_type: What we analyse, i.e. winner bid, ROI etc.
    :param file_name: The name of the file where the data is stored.
    """
    metrics_data = pd.read_csv(file_name)

    # Separating the data based on the winner type and extracting only what's important
    csv_data = {
        'a': list(metrics_data[data_type][metrics_data[agent_type] == 'a']),
        'b': list(metrics_data[data_type][metrics_data[agent_type] == 'b']),
        'c': list(metrics_data[data_type][metrics_data[agent_type] == 'c']),
        'd': list(metrics_data[data_type][metrics_data[agent_type] == 'd'])
    }

    # Visualisation
    data_for_frame = {}
    size = 10

    for element in ['a', 'b', 'c', 'd']:
        if len(csv_data[element]) > size:
            data_for_frame[element] = random.sample(csv_data[element], size)

    data_to_plot = pd.DataFrame(data_for_frame)

    # Shows a histogram
    data_to_plot.plot.hist()

    # Shows a Bell Curve
    data_to_plot.plot.kde()

    plt.show()


# TODO: Figure out what to do if certain groups don't have values.
def analyse_data(*args):
    """
    Analyses the given data in terms of ANOVA test.

    :param args: The data to be analysed
    :return:
    """

    # One-way ANOVA
    f_statistics, p = stats.f_oneway(args)

    print('f_statistics-Statistic={0}.3f,p={1}.3f'.format(f_statistics, p))
