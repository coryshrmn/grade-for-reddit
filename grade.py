#!/usr/bin/python3

import sys
import os

from textstat import textstat as ts
import json
import praw

cred = json.load(open('cred.json'))

out_name = 'out.txt'
if os.path.isfile(out_name):
    raise Exception('file "%s" already exists"' % out_name)

out = open(out_name, "w")

reddit = praw.Reddit(client_id=cred['client_id'],
    client_secret=cred['client_secret'],
    user_agent=cred['user_agent'])

sub_limit = 200
post_limit = 2000

subs = [sub.display_name for sub in reddit.subreddits.popular(limit=sub_limit)]
subs.append('dataisbeautiful')
subs.append('trees')
subs.append('askscience')
subs.append('askhistorians')
subs.append('askouija')
subs.append('geopolitics')
subs.append('democrats')
subs.append('republican')
subs.append('libertarian')
subs.append('conservative')
subs.append('progressive')
subs.append('socialism')
subs.append('feminism')
subs.append('communist')
subs.append('gonewild')

subs = list(map(lambda s: s.lower(), subs))
subs = sorted(set(subs))

sub_limit = len(subs)

# header
print("subreddit\tsentence_count\tword_count\tsyllable_count\ttrisyllabic_word_count\tfk_grade\tsmog_index", file=out)

def parse_comment(subreddit_name, body):
    # raw metrics
    sentences = ts.sentence_count(body)
    words = ts.lexicon_count(body)
    syllables = ts.syllable_count(body)
    trisyllabic = ts.trisyllab_count(body)

    # derived
    fk_grade = ts.flesch_kincaid_grade(body)
    smog = ts.smog_index(body)

    return (sub.display_name, sentences, words, syllables, trisyllabic, fk_grade, smog)

for (sub_i, sub) in enumerate(subs, 1):
    sub = reddit.subreddit(sub)
    posts = sub.top(time_filter='month', limit=post_limit)
    for (post_i, post) in enumerate(posts, 1):
        for comment in post.comments.list():
            if isinstance(comment, praw.models.Comment):
                try:
                    fields = parse_comment(sub.display_name, comment.body)
                except:
                    continue
                line = '\t'.join([str(x) for x in fields])
                print(line, file=out)
        # echo progress
        print("sub %3d/%3d; post %4d/%4d" % (sub_i, sub_limit, post_i, post_limit))
