#!/usr/bin/python3

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

fname = 'stats.txt'
hist_min = -3.5
hist_max = 20.5
hist_increment = 0.5
hist_bins = np.arange(hist_min, hist_max + hist_increment, hist_increment)

# the last "bin" is not a real bin, it's the max
hist_size = len(hist_bins) - 1

input_dtype = [('name', 'U21'), ('median', float), ('hist', int, (hist_size,))]
stats = np.loadtxt(fname, skiprows=1, dtype=input_dtype)

# put highest grade subreddits on top
stats = np.flip(stats, 0)

print(stats.shape)

extent = [hist_bins[0], hist_bins[-1], 0, len(stats)]
fig, ax = plt.subplots()

# plot histogram heatmap

def normalize_hist(hist):
    # normalize between subs, since they have different total comments
    total_per_sub = np.apply_along_axis(np.sum, 1, hist)

    # each row sums to 1
    return (hist.transpose() / total_per_sub).transpose()

# scale x logarithmically
# x=0   -> 0
# x=mid -> 0.5
# x=max -> 1.0
def log_scale(x, mid, max):
    scale = (max - 2 * mid) / (mid ** 2)

    return np.log1p(x * scale) / np.log1p(max * scale)

# mid and max are the same as passed into log_scale
# y is the result of log_scale(x, mid, max)
# returns x
def invert_log_scale(y, mid, max):
    scale = (max - 2 * mid) / (mid ** 2)

    return ((max * scale + 1) ** y - 1) / scale

def log_hist(norm_hist):

    median = np.mean(norm_hist)
    mx = np.max(norm_hist)

    # scale such that the median becomes 0.5 after log
    scale = (mx - 2 * median) / (median ** 2)

    # logarithmic, and divide to bring into range 0-1
    hist = np.log1p(norm_hist * scale)
    return hist / hist.max()


hist = stats['hist'].astype(float)
hist = normalize_hist(hist)
scale_mid = np.percentile(hist, 90)
scale_max = np.max(hist)

print('old min: ' + str(np.min(hist)))
print('old max: ' + str(np.max(hist)))
print('old median: ' + str(np.median(hist)))
print('old mean: ' + str(np.mean(hist)))

hist = log_scale(hist, scale_mid, scale_max)

print('new min: ' + str(np.min(hist)))
print('new max: ' + str(np.max(hist)))
print('new median: ' + str(np.median(hist)))
print('new mean: ' + str(np.mean(hist)))

cax = ax.imshow(hist, cmap="inferno", extent=extent, aspect='auto')

ax.set_title('Grade Levels for Reddit Comment Comprehension', y=1.04)
ax.set_xlabel('Grade Level')

# display xticks at top too
ax.tick_params(top=True, labeltop=True)

# tick each integer grade level
ax.xaxis.set_major_locator(plticker.MultipleLocator(base=1))

ax.tick_params(left=False, labelleft=False)

# add a plus to the last label, since the final histogram bin includes to infinity
xticks = [int(x) for x in ax.get_xticks().tolist()]
xticks[-2] = str(int(hist_max)) + '+'
ax.set_xticklabels(xticks, ha='left')

# draw subreddit name labels
label_x = -3.7
for i, row in enumerate(stats):
    name = row['name']
    median = row['median']
    y = len(stats) - i - 0.5

    label = "%s (%.1f)" % (name, median);
    ax.text(label_x, y, label, horizontalalignment='right', verticalalignment='center')

cbar_ticks = np.linspace(0, 1, num=10)
cbar_tick_labels = ['%.1f%%' % (100 * invert_log_scale(v, scale_mid, scale_max)) for v in cbar_ticks]
cbar = fig.colorbar(cax, ticks=cbar_ticks, orientation='horizontal', fraction=0.035, pad=0.08)
cbar.set_label('Comments in Subreddit')
cbar.ax.set_xticklabels(cbar_tick_labels)

plt.show()
