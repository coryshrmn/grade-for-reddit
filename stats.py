#!/usr/bin/python3

import os

import numpy as np

out_name = 'stats.txt'
if os.path.isfile(out_name):
    raise Exception('file "%s" already exists"' % out_name)

out = open(out_name, 'w')

# 0th column is subreddit name, 5th column is fk grade
input_dtype = [('name', 'U21'), ('score', float)]
fname = 'grades.txt'
data = np.loadtxt(fname, skiprows=1, usecols=(0,5), dtype=input_dtype)

hist_min = -3.5
hist_max = 20.5
hist_increment = 0.5

hist_bins = np.arange(hist_min, hist_max + hist_increment, hist_increment)
# each score is rounded to 0.1, offset the bins to prevent rounding error
hist_bins -= 0.05
# the last bin should catch all grades
hist_bins[-1] = float('inf')

# the last "bin" is not a real bin, it's the max
hist_size = len(hist_bins) - 1

names = np.unique(data['name'])

# stats is (median, histogram...)
stats_dtype = [('median', float), ('hist', int, hist_size)]
stats = np.empty(len(names), dtype=stats_dtype)


for i, name in enumerate(names):
    mask = data['name'] == name
    scores = data[mask]['score']

    median = np.median(scores)
    hist, _ = np.histogram(scores, bins=hist_bins)

    stats[i]['median'] = median
    stats[i]['hist'] = hist

# sort by median
sort = stats['median'].argsort()
stats = stats[sort]
names = names[sort]

# header
print('subreddit\tmedian\thistogram...', file=out)

# rows
for (i, name) in enumerate(names):
    row = stats[i]
    fields = [name] + [str(row['median'])] + [str(v) for v in row['hist']]
    line = '\t'.join(fields)
    print(line, file=out)
