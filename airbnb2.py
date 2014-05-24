import pandas as pd
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
duplicate_counts = duplicates.groupby(['landing_page']).count() # new = 4759, old = 4761

uniques = experiment.groupby(['user_id']).filter(lambda x: len(x) == 1)
unique_conversions = uniques.groupby(['landing_page']).sum() # new = 9527, old = 9049
unique_counts = uniques.groupby(['landing_page']).count() # new = 90815, old = 90813

old_count = unique_counts.ix['old_page', 'converted'] + duplicate_counts.ix['old_page', 'converted']
old_conv = unique_conversions.ix['old_page', 'converted'] + duplicate_conversions.ix['old_page', 'converted']
new_count = unique_counts.ix['new_page', 'converted']
new_conv = unique_conversions.ix['new_page', 'converted']

old_conv_rate = old_conv / old_count
new_conv_rate = new_conv / new_count

total_conv_rate = (old_conv + new_conv) / (old_count + new_count)
stdev = (total_conv_rate * (1 - total_conv_rate) / (old_count + new_count))**0.5
Z_new_page = (new_conv_rate - old_conv_rate) / stdev

print(old_conv_rate)
print(new_conv_rate)
print(total_conv_rate, stdev, Z_new_page)

'''
total_conv_rate = 0.102350460596
stdev = 0.000702082531901
Z_new_page = 7.09746213775
'''


####


# concatenate unique list with the unique version of the duplicates
country = pd.read_csv('country.csv').drop_duplicates()
experiment = pd.merge(experiment, pd.read_csv('country.csv'), on='user_id').drop_duplicates()

duplicates = experiment.groupby(['user_id']).filter(lambda x: len(x) > 1)
duplicate_conversions = duplicates.groupby(['landing_page', 'country']).sum()
duplicate_counts = duplicates.groupby(['landing_page', 'country']).count()

uniques = experiment.groupby(['user_id']).filter(lambda x: len(x) == 1)
unique_conversions = uniques.groupby(['landing_page', 'country']).sum()
unique_counts = uniques.groupby(['landing_page', 'country']).count()

old_counts = unique_counts.unstack().ix['old_page'].ix['converted'] + duplicate_counts.unstack().ix['old_page'].ix['converted']
old_convs = unique_conversions.unstack().ix['old_page'].ix['converted'] + duplicate_conversions.unstack().ix['old_page'].ix['converted'] 
new_counts = unique_counts.unstack().ix['new_page'].ix['converted']
new_convs = unique_conversions.unstack().ix['new_page'].ix['converted']

old_conv_rate = old_convs / old_counts
new_conv_rate = new_convs / new_counts

total_conv_rate = (old_convs + new_convs) / (old_counts + new_counts)
stdev = (total_conv_rate * (1 - total_conv_rate) / (old_counts + new_counts))**0.5
Z_new_page = (new_conv_rate - old_conv_rate) / stdev

print(old_conv_rate)
print(new_conv_rate)
print(total_conv_rate, stdev, Z_new_page)

'''
total_conv_rate
CA         0.102285
UK         0.103299
US         0.102682

stdev
CA         0.001749
UK         0.001358
US         0.000959

t_new_page
CA         0.936811
UK         0.857107
US         8.639609


##


unique_conversions
new_page     CA       1508
             UK       2532
             US       5235
old_page     CA       1480
             UK       2506
             US       4798

unique_counts
new_page     CA       14623
             UK       24370
             US       48962
old_page     CA       14622
             UK       24561
             US       48740

duplicate_conversions
new_page     CA       0
             UK       0
             US       0
old_page     CA       83
             UK       147
             US       262

duplicate_counts
new_page     CA       779
             UK       1263
             US       2557
old_page     CA       779
             UK       1263
             US       2559
'''