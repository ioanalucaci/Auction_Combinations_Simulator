"""
    Presents the information as a bell curve and histogram.
"""
import random
import matplotlib.pyplot as plt
import information_extractor as ie
import pandas as pd


# Visualisation
data_for_frame = {}
size = 10

csv_data = ie.extract_information()

for element in ['A', 'B', 'C', 'D']:
    if len(csv_data[element]) > size:
        data_for_frame[element] = random.sample(csv_data[element], size)

data_to_plot = pd.DataFrame(data_for_frame)

# Shows a histogram
data_to_plot.plot.hist()

# Shows a Bell Curve
data_to_plot.plot.kde()

plt.show()
