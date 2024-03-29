"""
Analyses the given data in terms of ANOVA test and visualises it.
"""
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def analyse_data(file_name, data_types, agent_types, types):
    """
    Analyses the data in terms of ANOVA tests and visualisation.

    :param file_name: the file name to be analysed
    :param data_types: the metric to be analysed
    :param agent_types: the agent type to be analysed
    :param types: the types that can be found in the file for the agent type
    :return:
    """
    metrics_data = pd.read_csv(file_name)

    for agent_type in agent_types:
        for data_type in data_types:
            csv_data = {}
            # Separating the data based on the winner type and extracting only what's important
            for element_type in types[agent_type]:
                csv_data[element_type] = list(metrics_data[data_type][metrics_data[agent_type] == element_type])

            visualise_data(csv_data, types[agent_type], data_type, agent_type)

            print("----------------------------------------------------------")
            print("ANOVA test for '{1}' in terms of '{0}':".format(agent_type, data_type))
            anova_test_data(csv_data, types[agent_type])
            print("----------------------------------------------------------")


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

    print('f_statistics={0}; p={1}'.format(f_statistics, p))


def visualise_data(csv_data, types, data_type, agent_type):
    """
    Prints out plots to show the metrics data.

    :param csv_data: The information to be printed.
    :param types: What types we are analysing
    :param data_type: the metric to be analysed
    :param agent_type: the agent type to be analysed
    """
    # Visualisation
    data_for_frame = {}
    data_for_bar = []

    for element in types:
        data_for_frame[element] = csv_data[element]
        data_for_bar.append(sum(csv_data[element]) / len(csv_data[element]))

    data_to_plot = pd.DataFrame(data_for_frame)
    data_to_bar_plot = pd.DataFrame({agent_type: types, data_type: data_for_bar})

    # Shows a Box with whiskers
    boxplot = sns.boxplot(x='variable', y='value', data=pd.melt(data_to_plot), order=data_for_frame.keys())

    boxplot.set_xlabel("", fontsize=16)
    boxplot.set_ylabel("", fontsize=16)

    for tick in boxplot.get_xticklabels():
        tick.set_fontsize(16)
    for tick in boxplot.get_yticklabels():
        tick.set_fontsize(16)

    # Shows a Bar Chart
    data_to_bar_plot.plot.bar(x=agent_type, y=data_type, rot=0)

    plt.show()
