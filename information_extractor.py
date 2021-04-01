from datetime import datetime
import pandas as pd


def extract_information():
    """
        Extract the required information from the CSV file.

        :return: the extracted information
    """
    today = datetime.today()
    data_type = 'Winner Satisfaction'
    agent_type = 'Winner Type'

    file_name = "metrics " + today.strftime('%d-%m-%y') + ".csv"

    metrics_data = pd.read_csv(file_name)

    # Separating the data based on the winner type and extracting only what's important
    return {
        'A': list(metrics_data[data_type][metrics_data[agent_type] == 'A']),
        'B': list(metrics_data[data_type][metrics_data[agent_type] == 'B']),
        'C': list(metrics_data[data_type][metrics_data[agent_type] == 'C']),
        'D': list(metrics_data[data_type][metrics_data[agent_type] == 'D'])
    }
