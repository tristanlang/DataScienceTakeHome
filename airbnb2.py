import pandas as pd
import numpy as np

experiment = pd.read_csv('experiment.csv')
#country = pd.read_csv('country.csv')

subexperiment = experiment.ix[:10000]


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
duplicates = experiment.groupby(experiment['user_id']).filter(lambda x: len(x) > 1)
duplicate_conversions = duplicates.groupby(duplicates['landing_page']).sum() # new = 0, old = 501
duplicate_counts = duplicates.groupby(duplicates['landing_page']).count() # new = 4761, old = 4759

print(duplicate_conversions)
print(duplicate_counts)
#print(duplicates.groupby(duplicates['landing_page']).sum())

uniques = experiment.groupby(experiment['user_id']).filter(lambda x: len(x) == 1)
unique_conversions = uniques.groupby(uniques['landing_page']).sum() # new = 9527, old = 9049
unique_counts = uniques.groupby(uniques['landing_page']).count() # new = 90815, old = 90813

#print(uniques)
print(unique_conversions)
print(unique_counts)