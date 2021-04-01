"""
Analyses the given data in terms of ANOVA test.
"""
from scipy import stats
from datetime import datetime
import data_visualiser as dv

today = datetime.today()
data_type = 'Winner Satisfaction'
agent_type = 'Winner Type'

file_name = "metrics " + today.strftime('%d-%m-%y') + ".csv"

csv_data = dv.extract_information(file_name, agent_type, data_type)

# One-way ANOVA
f_statistics, p = stats.f_oneway(csv_data['A'], csv_data['B'])

print('f_statistics-Statistic={0}.3f,p={1}.3f'.format(f_statistics, p))
