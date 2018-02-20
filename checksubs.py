#!/usr/bin/env python3

# prints sub counts, to make sure I typed names correctly

import urllib.request
import json
from time import sleep

subs = []
subs.append('dataisbeautiful')
subs.append('data_irl')
subs.append('trees')
subs.append('askscience')
subs.append('askhistorians')
subs.append('askouija')
subs.append('geopolitics')
subs.append('democrats')
subs.append('republican')
subs.append('libertarian')
subs.append('conservative')
subs.append('conservatives')
subs.append('anarchism')
subs.append('voluntarism')
subs.append('enoughtrumpspam')
subs.append('enoughobamaspam')
subs.append('prochoice')
subs.append('progun')
subs.append('conspiracy')
subs.append('mensrights')
subs.append('watchpeopledie')
subs.append('peoplefuckingdying')
subs.append('nsfw')
subs.append('liberal')
subs.append('progressive')
subs.append('socialism')
subs.append('feminism')
subs.append('communism')
subs.append('gonewild')
subs.append('asksocialscience')
subs.append('askanthropology')
subs.append('askacademia')
subs.append('history')


for sub in subs:
    page = urllib.request.urlopen("https://www.reddit.com/r/%s/about.json" % sub)
    j = json.load(page)
    print("%s: %d" % (sub, j['data']['subscribers']))
    sleep(2)
