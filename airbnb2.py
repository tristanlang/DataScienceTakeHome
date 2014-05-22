import pandas as pd
from pandas import DataFrame
import numpy as np


# get the list of users that saw both pages
# ==> a subset of the treatment group ends up seeing both pages
# ==> each of the users in this subset hits the new_page first
# ==> BUT one second later they hit the old_page
# 
# analysis of the old_page vs new_page conversions show that there are no new_page conversions
# ==> the users likely never actually saw the new_page and probably only saw the old_page
# 
# 4760 duplicates
# 0 conversions when hitting new_page
# 501 conversions when hitting old_page
experiment = pd.read_csv('experiment.csv')

duplicates = experiment.groupby(['user_id']).filter(lambda x: len(x) > 1)
duplicate_conversions = duplicates.groupby(['landing_page']).sum() # new = 0, old = 501
duplicate_counts = duplicates.groupby(['landing_page']).count() # new = 4761, old = 4759

uniques = experiment.groupby(['user_id']).filter(lambda x: len(x) == 1)
unique_conversions = uniques.groupby(['landing_page']).sum() # new = 9527, old = 9049
unique_counts = uniques.groupby(['landing_page']).count() # new = 90815, old = 90813

old_count = unique_counts.ix['new_page', 'converted'] + duplicate_counts.ix['new_page', 'converted']
old_conv = unique_conversions.ix['old_page', 'converted'] + duplicate_conversions.ix['old_page', 'converted']
new_count = unique_counts.ix['new_page', 'converted']
new_conv = unique_conversions.ix['new_page', 'converted']

old_conv_rate = (unique_conversions.ix['old_page', 'converted'] + duplicate_conversions.ix['old_page', 'converted']) / (unique_counts.ix['new_page', 'converted'] + duplicate_counts.ix['new_page', 'converted'])
new_conv_rate = unique_conversions.ix['new_page', 'converted'] / unique_counts.ix['new_page', 'converted']

total_conv_rate = (old_conv + new_conv) / (old_count + new_count)
stdev = (total_conv_rate * (1 - total_conv_rate) / (old_count + new_count))**0.5
t_new_page = (new_conv_rate - old_conv_rate) / stdev

print(total_conv_rate, stdev, t_new_page)


####


# concatenate unique list with the unique version of the duplicates
country = pd.read_csv('country.csv').drop_duplicates()
experiment = pd.merge(experiment, pd.read_csv('country.csv'), on='user_id').drop_duplicates()
#print(experiment)

'''
NEXT STEPS:
-perform same sort of duplicate and unique counts and conversion sums for the datasets with country
-group by country
-look at conv rates and counts by country
'''
duplicates = experiment.groupby(['user_id']).filter(lambda x: len(x) > 1)
duplicate_conversions = duplicates.groupby(['landing_page', 'country']).sum() # new = 0, old = 501
duplicate_counts = duplicates.groupby(['landing_page', 'country']).count() # new = 4761, old = 4759

uniques = experiment.groupby(['user_id']).filter(lambda x: len(x) == 1)
unique_conversions = uniques.groupby(['landing_page', 'country']).sum() # new = 9527, old = 9049
unique_counts = uniques.groupby(['landing_page', 'country']).count() # new = 90815, old = 90813

'''old_count = unique_counts.ix['new_page', 'converted'] + duplicate_counts.ix['new_page', 'converted']
old_conv = unique_conversions.ix['old_page', 'converted'] + duplicate_conversions.ix['old_page', 'converted']
new_count = unique_counts.ix['new_page', 'converted']
new_conv = unique_conversions.ix['new_page', 'converted']

old_conv_rate = (unique_conversions.ix['old_page', 'converted'] + duplicate_conversions.ix['old_page', 'converted']) / (unique_counts.ix['new_page', 'converted'] + duplicate_counts.ix['new_page', 'converted'])
new_conv_rate = unique_conversions.ix['new_page', 'converted'] / unique_counts.ix['new_page', 'converted']

total_conv_rate = (old_conv + new_conv) / (old_count + new_count)
stdev = (total_conv_rate * (1 - total_conv_rate) / (old_count + new_count))**0.5
t_new_page = (new_conv_rate - old_conv_rate) / stdev

print(total_conv_rate, stdev, t_new_page)'''