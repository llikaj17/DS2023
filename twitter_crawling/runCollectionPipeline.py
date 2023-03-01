import json
import pandas as pd
from TwitterAPI import collect_twitter_data
from dataPreprocessing import clean_text
from configKeywords import configs

print('\n>>   Welcome to the Twitter Collection Pipeline  <<')
print('____________________________________________________\n')

topic_select = ['covid', 'trump']
select_message = '>> \tPlease, select one of the following topics. Press 1, 2: \n'
for i, select in enumerate(topic_select):
    select_message += '\t\t' + str(i+1) + '. ' + select + '\n'
select_message += '>>\t Select: '
input_selected = input(select_message)
try:
    selected = int(input_selected)
    if selected < 1 or selected > 2:
        print('>>\tYour selection is out of range. '
              '[ERROR]Please make sure your input is 1, 2, or 3. corresponding to the desired topic.')
        exit(-1)
except Exception as e:
    print('>>\t[ERROR]Unknown value entered. Please make sure your input is 1, 2, or 3 corresponding to the desired topic.')
    print('Try again!')
    exit(-1)

# Define the keywords
# TODO: All hardcoded dictionaries should be external files to simplify maintenance
hate_keywords = "#bitch " \
                   "OR fake pandemic " \
                   "OR slut " \
                   "OR #blm " \
                   "OR feminismcancer " \
                   "OR feminismterrorism " \
                   "OR #killblacks " \
                   "OR #fucktrump " \
                   "OR #fuckblm " \
                   "OR #trumbitch " \
                   "OR #trumpgays " \
                   "OR #killlgbt " \
                   "OR #murdergays " \
                   "OR gay " \
                "OR lgbt " \
                "OR allahsoil " \
                "OR protest " \
                "OR muslim " \
                "OR nazi " \
                "OR antiamerican "
trump_keywords = "Trump OR #trump OR #notmypresident OR #election2020 OR #donaldtrump OR #liberals "

selected_topic = topic_select[selected-1]
topic = configs[selected_topic]
topic_keywords = topic['topic_keywords']
hate_keywords = topic['hate_keywords']

search_keywords = ' '.join([topic_keywords, hate_keywords])

# Collect data from Twitter API
tweets_data = collect_twitter_data(search_keywords)

# Preprocess tweets (Cleaning, removing emojis, divide words, split hash tags etc...)
print('>>   Cleaning data...    <<')
clean_tweet_df = tweets_data.apply(lambda tweet: clean_text(tweet['tweets']), axis=1)
clean_tweet_df.to_csv('clean_tweets.csv')
print('\n>>   Process Finished Successfully!    <<')

# Further analysis on location
# Compound words split
# Double words analysis?


