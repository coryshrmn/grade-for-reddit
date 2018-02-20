#!/usr/bin/python3

import sys
import os

from textstat import textstat as ts
import json
import praw

cred = json.load(open('cred.json'))
in_name = 'subs.txt'
out_name = 'grades.txt'

if os.path.isfile(out_name):
    raise Exception('file "%s" already exists"' % out_name)

out = open(out_name, "w")

# reddit API seems to limit to 1000
post_limit = 2000

# read sub list
with open(in_name) as infile:
    lines = infile.readlines()

subs = [l.strip() for l in lines]
subs = list(filter(lambda s: len(s) > 0, subs))
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

reddit = praw.Reddit(client_id=cred['client_id'],
    client_secret=cred['client_secret'],
    user_agent=cred['user_agent'])

for (sub_i, sub) in enumerate(subs, 1):
    print("sub: %s" % sub)
    sub = reddit.subreddit(sub)
    posts = sub.top(time_filter='month', limit=post_limit)
    for (post_i, post) in enumerate(posts, 1):
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            try:
                fields = parse_comment(sub.display_name, comment.body)
            except:
                continue
            line = '\t'.join([str(x) for x in fields])
            print(line, file=out)
        # echo progress
        print("sub %3d/%3d; post %4d/%4d" % (sub_i, sub_limit, post_i, post_limit))
