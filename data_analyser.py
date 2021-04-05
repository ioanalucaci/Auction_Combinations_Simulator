"""
Analyses the given data in terms of ANOVA test and visualises it.
"""
from scipy import stats
import pandas as pd
import random
import matplotlib.pyplot as plt


def analyse_data(file_name, data_type, agent_type, types):
    """
    Analyses the data in terms of ANOVA tests and visualisation.

    :param file_name: the file name to be analysed
    :param data_type: the metric to be analysed
    :param agent_type: the agent type to be analysed
    :param types: the types that can be found in the file for the agent type
    :return:
    """
    metrics_data = pd.read_csv(file_name)
    csv_data = {}

    # Separating the data based on the winner type and extracting only what's important
    for element_type in types:
        csv_data[element_type] = list(metrics_data[data_type][metrics_data[agent_type] == element_type])

    visualise_data(csv_data, types)

    anova_test_data(csv_data, types)


def anova_test_data(csv_data, types):
    """
    Applies ANOVA tests to the data

    :param csv_data: The data to go through the ANOVA test.
    :param types: The different groups to be tested.
    :return:
    """
    f_statistics, p = 0, 0

    if len(types) == 2:
        f_statistics, p = stats.f_oneway(csv_data[types[0]], csv_data[types[1]])
    elif len(types) == 3:
        f_statistics, p = stats.f_oneway(csv_data[types[0]], csv_data[types[1]], csv_data[types[2]])
    elif len(types) == 4:
        f_statistics, p = stats.f_oneway(csv_data[types[0]], csv_data[types[1]], csv_data[types[2]], csv_data[types[3]])

    print('f_statistics={0}.3f,p={1}.3f'.format(f_statistics, p))


def visualise_data(csv_data, types):
    """
    Prints out plots to show the metrics data.

    :param csv_data: The information to be printed.
    :param types: What types we are analysing
    """
    # Visualisation
    data_for_frame = {}
    size = 10

    for element in types:
        if len(csv_data[element]) > size:
            data_for_frame[element] = random.sample(csv_data[element], size)

    data_to_plot = pd.DataFrame(data_for_frame)

    # Shows a histogram
    data_to_plot.plot.hist()

    # Shows a Bell Curve
    data_to_plot.plot.kde()

    plt.show()
