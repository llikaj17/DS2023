import tweepy as tw
import pandas as pd
import os
from configKeywords import configs

"""
Reference: Developer Account Twitter: https://developer.twitter.com/en
Documentation Twitter API v2: https://developer.twitter.com/en/docs
Documentation Tweepy: https://www.tweepy.org/
"""


def collect_twitter_data(key_words, date_since="2022-1-16", limit=1000):
    # You can change the dates in the configKeywords file accordingly
    if len(configs['date']) is not '':
        date_since = configs['date']

    # Get api keys from environmental variable
    # Note: If you want to run this methods you need to have access to Twitter API
    # For security reasons we store them only on our environmental variables
    print('>>   Connecting to the Twitter API...    <<')
    consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
    consumer_secret = os.environ.get('TWITTER_SECRET_KEY')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    print('>>   Connected Successfully!  <<')

    # Search Twitter for Tweets
    search_words = key_words
    # Define a query on Search term - in this case #bonn and the start date of your search
    # Retweets Filter - To keep or remove retweets
    query = search_words + " -filter:retweets since:" + date_since

    # Collect tweets
    print('>>   Scrape data from Twitter API     <<')
    tweets = tw.Cursor(api.search_tweets,
                       q=query,
                       lang="en",
                       tweet_mode='extended').items(limit)

    # Collect a list of tweets and convert to pandas dataframe
    # Get user location of related tweets for further preprocessing of data (Finding most affected region etc...)
    # Date object: Output will be a datetime object. - tweet.created_at
    raw_tweet_list = [[tweet.full_text, tweet.user.screen_name, tweet.user.location] for tweet in tweets]
    raw_tweet_df = pd.DataFrame.from_records(data=raw_tweet_list, columns=['tweets', 'username', 'location'])
    # Comment this line in case you want to store tweets to the same directory
    location = 'collected-tweets/' + date_since + '_raw_tweets.csv'
    raw_tweet_df.to_csv(location)
    print('>>   Collected data stored in: ' + location + ".  <<")

    return raw_tweet_df
