import pandas as pd
import os

pd.set_option("display.max_rows", 10, "display.max_columns", None)
dfs = pd.read_csv("all_merged_tweets.csv")
dfs['label'][~dfs['label'].isnull()].astype(int)
print(dfs.groupby('label').size())
print(len(dfs))
dfs = dfs.drop_duplicates(subset=['tweets', 'username'], keep='first')
dfs['label'][~dfs['label'].isnull()].astype(int)
print(dfs.head())


dfs = dfs.reset_index()
dfs = dfs.drop(columns=['Unnamed: 0', 'index'])
print(dfs.groupby('label').size())
print(len(dfs))
dfs.to_csv('trump_merged_tweets.csv')

