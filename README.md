# DS2023
Seminar in Data Science

This is the repo for the seminar report with the collected tweets, crawling tool and datasets used for training LSTM BiLSTM networks

- LSTM_BiLSTM_Detoxify: contains notebook to train and evaluate LSTMs networks and use Detoxify to classify our collected tweets
- datasets: contains train and test.cvs from Kaggle https://www.kaggle.com/datasets/arkhoshghalb/twitter-sentiment-analysis-hatred-speech
- twitter_crawling: contains scripts to scrape tweets from Twitter
- crawled_tweets: contains tweets that were collected using Twitter API


---

To run the twitter crawling tool:

- Run run_collection_pipeline.py 
- Make sure you have set environmental variable such as Twitter API Key, and proper endpoint URLs to access the API


        consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
        consumer_secret = os.environ.get('TWITTER_SECRET_KEY')
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
