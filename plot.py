#!/usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

# 0th column is subreddit name, 5th column is fk grade
input_dtype = [('name', 'S21'), ('score', float)]
fname = 'grades.txt'
data = np.loadtxt(fname, skiprows=1, usecols=(0,5), dtype=input_dtype)

hist_min = -3.5
hist_max = 20.5
hist_increment = 0.5

hist_bins = np.arange(hist_min, hist_max + hist_increment, hist_increment)
view_bins = np.copy(hist_bins)
# each score is rounded to 0.1, offset the bins to prevent rounding error
hist_bins -= 0.05
# the last bin should catch all grades
hist_bins[-1] = float('inf')

# the last "bin" is not a real bin, it's the max
hist_size = len(hist_bins) - 1

names = np.unique(data['name'])

# stats is (name_id, median, histogram...)
stats = np.empty([len(names), 2 + hist_size])

for i, name in enumerate(names):
    mask = data['name'] == name
    scores = data[mask]['score']

    median = np.median(scores)
    hist, _ = np.histogram(scores, bins=hist_bins)

    hist = hist / hist.max()

    stats[i,0] = i
    stats[i,1] = median
    stats[i,2:] = hist

# sort by median
stats = stats[stats[:,1].argsort()]

extent = [view_bins[0], view_bins[-1], 0, len(names)]
fig, ax = plt.subplots()
ax.set_xlim(extent[0], extent[1])
ax.set_ylim(extent[2], extent[3])

# plot histogram heatmap
ax.imshow(stats[:,2:], cmap="inferno", extent=extent)

# display xticks at top too
ax.tick_params(top=True, labeltop=True)

# tick each integer grade level
ax.xaxis.set_major_locator(plticker.MultipleLocator(base=1))

ax.tick_params(left=False, labelleft=False)

# add a plus to the last label, since the final histogram bin includes to infinity
xticks = [int(x) for x in ax.get_xticks().tolist()]
xticks[-2] = str(int(hist_max)) + '+'
ax.set_xticklabels(xticks)

# draw subreddit name labels
label_x = -3.7
for r in range(len(names)):
    name = names[int(stats[r, 0])]
    median = stats[r, 1]

    label = "%s (%.1f)" % (name.decode('utf-8'), median);

    y = len(names) - r - 0.5
    ax.text(label_x, y, label, horizontalalignment='right', verticalalignment='center')

plt.show()
