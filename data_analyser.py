import pandas as pd
import random
import matplotlib.pyplot as plt
from scipy import stats


def analyse_winner():
    metrics_data = pd.read_csv('metrics 22-03-21.csv')

    # Separating the data based on the winner type and extracting only the winning bid
    anova_data = {
        'a': list(metrics_data['Winning Bid'][metrics_data['Winner Type'] == 'a']),
        'b': list(metrics_data['Winning Bid'][metrics_data['Winner Type'] == 'b']),
        'c': list(metrics_data['Winning Bid'][metrics_data['Winner Type'] == 'c']),
        'd': list(metrics_data['Winning Bid'][metrics_data['Winner Type'] == 'd'])
    }

    # One-way ANOVA
    f_statistics, p = stats.f_oneway(anova_data['a'], anova_data['b'], anova_data['c'], anova_data['d'])

    print('f_statistics-Statistic={0}.3f,p={1}.3f'.format(f_statistics, p))

    # Visualisation
    size = min(len(anova_data['a']), len(anova_data['b']), len(anova_data['c']), len(anova_data['d']))

    data_to_plot = pd.DataFrame({'a': random.sample(anova_data['a'], size),
                                 'b': random.sample(anova_data['b'], size),
                                 'c': random.sample(anova_data['c'], size),
                                 'd': random.sample(anova_data['d'], size)})

    # Shows a histogram
    data_to_plot.plot.hist()

    # Shows a Bell Curve
    data_to_plot.plot.kde()

    plt.show()
