#!/usr/bin/python3

import sys

from textstat.textstat import textstat
import json
import praw

cred = json.load(open('cred.json'))

reddit = praw.Reddit(client_id=cred['client_id'],
    client_secret=cred['client_secret'],
    user_agent=cred['user_agent'])

sub_count = 100
post_count = 100

subs = [sub.display_name for sub in reddit.subreddits.popular(limit=100)]
print(subs)

sub_i = 0
for sub in subs:
    sub_i += 1
    sub = reddit.subreddit(sub)
    post_i = 0
    for post in sub.hot(limit=100):
        post_i += 1
        for comment in post.comments.list():
            if isinstance(comment, praw.models.Comment):
                body = comment.body
                try:
                    grade = textstat.flesch_kincaid_grade(body)
                    print("%s\t%s" % (sub.display_name, grade))
                except:
                    pass
        print("sub %03d/%03d; post %03d/%03d" % (sub_i, sub_count, post_i, post_count), file=sys.stderr)
