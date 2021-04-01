"""
Analyses the given data in terms of ANOVA test.
"""
from scipy import stats
import information_extractor as ie


csv_data = ie.extract_information()

# One-way ANOVA
f_statistics, p = stats.f_oneway(csv_data['A'], csv_data['B'])

print('f_statistics-Statistic={0}.3f,p={1}.3f'.format(f_statistics, p))
