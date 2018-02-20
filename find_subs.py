#!/usr/bin/python3

import os
import json

import praw

cred = json.load(open('cred.json'))

out_name = 'subs.txt'
if os.path.isfile(out_name):
    raise Exception('file "%s" already exists"' % out_name)

out = open(out_name, "w")

reddit = praw.Reddit(client_id=cred['client_id'],
    client_secret=cred['client_secret'],
    user_agent=cred['user_agent'])

sub_limit = 200

subs = [sub.display_name for sub in reddit.subreddits.popular(limit=sub_limit)]
subs.append('dataisbeautiful')
subs.append('dataisbeautiful')
subs.append('data_irl')
subs.append('trees')
subs.append('askscience')
subs.append('askhistorians')
subs.append('asksocialscience')
subs.append('askanthropology')
subs.append('askacademia')
subs.append('history')
subs.append('askouija')
subs.append('geopolitics')
subs.append('democrats')
subs.append('republican')
subs.append('libertarian')
subs.append('conservative')
subs.append('anarchism')
subs.append('enoughtrumpspam')
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

subs = list(map(lambda s: s.lower(), subs))
subs = sorted(set(subs))

print('\n'.join(subs), file=out)
