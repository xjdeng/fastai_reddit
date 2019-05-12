import praw
import pandas as pd
import sys
import re
import bs4
import markdown

credential_file = "credentials.key"

try:
    with open(credential_file, 'r') as f:
        creds = f.read().split('\n')
    personal = creds[0]
    secret = creds[1]
    username = creds[2]
    password = creds[3]
except IOError as e:
    print("You didn't create a credential file! Please see sample_credentials.key")
    print("Then go to http://www.storybench.org/how-to-scrape-reddit-with-python/")
    print("And register a new app named fastai_reddit in your reddit account.")
    print("And insert the values into sample_credentials.key and save it as {}.".format(credential_file))
    raise(e)

reddit = praw.Reddit(client_id=personal, client_secret=secret, user_agent='fastai_reddit', username=username, \
                     password=password)

def get_posts(sub):
    subreddit = reddit.subreddit(sub)
    top = list(subreddit.top(limit=1000))
    new = list(subreddit.new(limit=1000))
    rising = list(subreddit.rising(limit=1000))
    controversial = list(subreddit.controversial(limit=1000))
    gilded = list(subreddit.gilded(limit=1000))
    allposts = list(set(top + new + rising + controversial + gilded))
    return allposts

def noquotes(text):
    """
This function first stated out as a way to remove markdown quotes from raw reddit markdown text but now it's more of a
general purpose text parser, but the name hasn't changed.
    """
    #https://stackoverflow.com/questions/761824/python-how-to-convert-markdown-formatted-text-to-text
    t1 = re.sub(">.+?(\n|$)","",text).replace("\\n","").replace("\\","")
    html = markdown.markdown(t1)
    t2 = ''.join(bs4.BeautifulSoup(html, 'lxml').findAll(text=True))
    
    return t2

def get_comment_text(comment, minchars = 200):
    comments = []
    if isinstance(comment, praw.models.MoreComments):
        newcomments = comment.comments()
        for n in newcomments:
            comments += get_comment_text(n, minchars)
    else:
        if len(comment.body) > minchars:
            comments.append(noquotes(comment.body))
    return comments

def parse_comments(posts, minchars = 200):
    alltext = []
    for p in posts:
        tmp = noquotes(p.selftext)
        if len(tmp) >= minchars:
            alltext.append(tmp)
        for c in p.comments.list():
            alltext += get_comment_text(c, minchars)
    return alltext

if __name__ == "__main__":
    sub = sys.argv[1]
    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    else:
        outfile = sub + ".csv"
    posts = get_posts(sub)
    text = parse_comments(posts)
    df = pd.DataFrame()
    df['subreddit'] = [sub]*len(text)
    df['text'] = text
    df.to_csv(outfile)