# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 18:18:50 2021

@author: YF
"""

'''============================================================================

Purpose: To analyze the sentiments of the reddit
This program uses Vader SentimentIntensityAnalyzer to calculate the ticker
compound value.
You can change multiple parameters to suit your needs. See below under "set
program parameters."
Implementation:
I am using sets for 'x in s' comparison, sets time complexity for "x in s" is
O(1) compare to list: O(n).
Limitations:
- It depends mainly on the defined parameters for current implementation:
- It completely ignores the heavily downvoted comments, and there can be a time
  when the most mentioned ticker is heavily downvoted, but you can change that
  in upvotes variable.
Author: github:asad70

============================================================================'''

import praw
from reddit_sentiment_config import *
import time as tm
import pandas as pd
import matplotlib.pyplot as plt
import squarify
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def analyse_sentiment():

    start_time = tm.time()
    reddit = praw.Reddit(
        user_agent="Comment Extraction",
        client_id="SkS62tuIvHhvFYOmSvqWhw",
        client_secret="vkna1ArgKOtzL8z_-l9yTbi2CZ0p9g"
    )

    # Set the program parameters ##############################################
    subs = ['wallstreetbets', 'stocks', 'investing', 'stockmarket'] # sub-reddit to search
    post_flairs = {'Daily Discussion', 'Weekend Discussion', 'Discussion'} # posts flairs to search || None flair is automatically considered
    goodAuth = {'AutoModerator'} # authors whom comments are allowed more than once
    uniqueCmt = True # allow one comment per author per symbol
    ignoreAuthP = {'example'} # authors to ignore for posts
    ignoreAuthC = {'example'} # authors to ignore for comment
    upvoteRatio = 0.70 # upvote ratio for post to be considered, 0.70 = 70%
    ups = 20 # define # of upvotes, post is considered if upvotes exceed this #
    limit = 10 # define the limit, comments 'replace more' limit
    upvotes = 2 # define # of upvotes, comment is considered if upvotes exceed this #
    picks = 10 # define # of picks here, prints as "Top ## picks are:"
    picks_ayz = 5 # define # of picks for sentiment analysis
    ###########################################################################


    posts, count, c_analyzed, tickers, titles, a_comments = 0, 0, 0, {}, [], {}
    cmt_auth = {}

    for sub in subs:
        subreddit = reddit.subreddit(sub)
        hot_python = subreddit.hot()    # sorting posts by hot

        # Extracting comments, symbols from subreddit
        for submission in hot_python:
            flair = submission.link_flair_text
            author = submission.author.name

            # Checking post upvote ratio, # of upvotes, post flair, and author
            if submission.upvote_ratio >= upvoteRatio and submission.ups > ups\
                and (flair in post_flairs or flair is None) \
                    and author not in ignoreAuthP:
                submission.comment_sort = 'new'
                comments = submission.comments
                titles.append(submission.title)
                posts += 1
                submission.comments.replace_more(limit=limit)
                for comment in comments:
                    # Try except for deleted account?
                    try: auth = comment.author.name
                    except: pass
                    c_analyzed += 1

                    # Checking comment upvotes and author
                    if comment.score > upvotes and auth not in ignoreAuthC:
                        split = comment.body.split(" ")
                        for word in split:
                            word = word.replace("$", "")
                            # upper = ticker,length of ticker<=5,excluded words
                            if word.isupper() and len(word) <= 5 and word \
                                not in blacklist and word in us:

                                # Unique comments, try/except for key errors
                                if uniqueCmt and auth not in goodAuth:
                                    try:
                                        if auth in cmt_auth[word]: break
                                    except: pass

                                # Counting tickers
                                if word in tickers:
                                    tickers[word] += 1
                                    a_comments[word].append(comment.body)
                                    cmt_auth[word].append(auth)
                                    count += 1
                                else:
                                    tickers[word] = 1
                                    cmt_auth[word] = [auth]
                                    a_comments[word] = [comment.body]
                                    count += 1

        # Sorts the dictionary
        symbols = dict(sorted(tickers.items(), key=lambda item: item[1], \
                              reverse = True))
        top_picks = list(symbols.keys())[0:picks]
        time = (tm.time() - start_time)

        # Print time taken
        print("It took {t:.2f} seconds to analyze {c} comments in \
              subreddit r\\{r} \n".format(t=time, c=c_analyzed, r=sub))
        # print("Posts analyzed saved in titles")
        # For i in titles: print(i)  # prints the title of the posts analyzed

        # print(f"\n{picks} most mentioned picks: ")
        times = []
        top = []
        for i in top_picks:
            # print(f"{i}: {symbols[i]}")
            times.append(symbols[i])
            top.append(f"{i}: {symbols[i]}")


        # Applying Sentiment Analysis
        scores, s = {}, {}

        vader = SentimentIntensityAnalyzer()
        # Adding custom words from data.py
        vader.lexicon.update(new_words)

        picks_sentiment = list(symbols.keys())[0:picks_ayz]
        for symbol in picks_sentiment:
            stock_comments = a_comments[symbol]
            for cmnt in stock_comments:
                score = vader.polarity_scores(cmnt)
                if symbol in s:
                    s[symbol][cmnt] = score
                else:
                    s[symbol] = {cmnt:score}
                if symbol in scores:
                    for key, _ in score.items():
                        scores[symbol][key] += score[key]
                else:
                    scores[symbol] = score

            # Calculating avg.
            for key in score:
                scores[symbol][key] = scores[symbol][key] / symbols[symbol]
                scores[symbol][key]  = "{pol:.3f}".format(pol=scores[symbol]\
                                                          [key])

        # printing sentiment analysis
        df = pd.DataFrame(scores)
        df.index = ['Bearish', 'Neutral', 'Bullish', 'Total/Compound']
        df = df.T

        # Date Visualization
        plt.clf()
        squarify.plot(sizes=times, label=top, alpha=.7 )
        plt.axis('off')
        plt.title(f"{picks} Most Mentioned Stocks on Reddit's r\\%s" %sub)
        plt.savefig('r_%s_top_picks.jpg' %sub, bbox_inches="tight")

        # Sentiment analysis
        plt.clf()
        df = df.astype(float)
        colors = ['red', 'dodgerblue', 'limegreen', 'gold']
        fig = df.plot(kind = 'bar', color=colors, title=f"Sentiment Analysis \
                      of Top {picks_ayz} Stocks on Reddit's r\\%s"  %sub)
        fig = fig.get_figure()
        fig.savefig('r_%s_sentiment.jpg' %sub, bbox_inches="tight")

if __name__ == analyse_sentiment():
    analyse_sentiment()