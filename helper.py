import tweepy
import sqlite3
import logging
from time import sleep
import os
from dotenv import load_dotenv
import praw
import requests

load_dotenv(override=True)

REDDIT_SECERET=os.getenv("REDDIT_SECERET")
REDDIT_CLIENTID=os.getenv("REDDIT_CLIENTID")

TWIT_APIKEY=os.getenv("TWIT_APIKEY")
TWIT_APISECRET=os.getenv("TWIT_APISECRET")
TWIT_BEARER=os.getenv("TWIT_BEARER")
TWIT_ACCESSTOKEN=os.getenv("TWIT_ACCESSTOKEN")
TWIT_ACCESSSECRET=os.getenv("TWIT_ACCESSSECRET")

SQL_DB = "result/data.db"

def execute_sql_file(file_path):
    """
    Reads and executes an SQL file.
    Args:
        file_path (str): Path to the SQL file.
    """
    # Connect to SQLite database
    conn = sqlite3.connect(SQL_DB)
    cursor = conn.cursor()

    with open(file_path, "r") as sql_file:
        sql_script = sql_file.read()
        cursor.executescript(sql_script)
        print(f"Executed {file_path} successfully.")
        logging.info(f"DB Table created use sql file: {file_path}")

    # Commit changes and close connection
    conn.commit()
    conn.close()


def scrape_reddit(subreddits):
    """
    Iterates through interested subreddits to scrape the hot 100 new posts and appends them to the DB
    Args:
        subreddits (List<String>): List of strings of Subreddits 
    """
    try:
        # Reddit API Object
        reddit_obj = praw.Reddit(
            client_id=REDDIT_CLIENTID,
            client_secret=REDDIT_SECERET,
            user_agent="MyAPI/0.0.1"
        )

        # Create connection to DB 
        conn = sqlite3.connect(SQL_DB)
        cursor = conn.cursor()

        # Scrape and upload to DB
        for subreddit_name in subreddits:
            subreddit = reddit_obj.subreddit(subreddit_name)
            # Extracts posts that are "hot" and trending by reddit showing greater influence
            for post in subreddit.hot(limit=100): 
                post_id = post.id
                title = post.title
                content = post.selftext
                subreddit = post.subreddit.display_name
                timestamp = post.created_utc
                author = post.author.name if post.author else "Deleted"
                
                # Insert into database
                cursor.execute("""
                INSERT OR IGNORE INTO reddit_data (id, title, content, subreddit, timestamp, author)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (post_id, title, content, subreddit, timestamp, author))
                
            logging.info(f"Reddit post collected for subreddit: {subreddit_name}")
            conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Error while scraping Reddit: {e}")

def scrape_twitter(twitter_keyword):
    """
    Searches for keywords in Twitter and appends it to DB
    Args:
        twitter_keyword (String):  Search term to search through Twitter.
    """
    try:
        twitter_obj = tweepy.Client(bearer_token=TWIT_BEARER, wait_on_rate_limit=True)

        max_results=10
        tweets = twitter_obj.search_recent_tweets(
            query=twitter_keyword,
            max_results=max_results,
            tweet_fields=["id", "text", "created_at", "author_id", "lang"]
        )

        conn = sqlite3.connect(SQL_DB)
        cursor = conn.cursor()

        if tweets.data:
            for tweet in tweets.data:
                id = tweet.id
                text = tweet.text
                created_at = tweet.created_at
                author_id = tweet.author_id
                lang = tweet.lang

                cursor.execute("""
                    INSERT OR IGNORE INTO twitter_data (id, text, created_at, author_id, lang)
                    VALUES (?, ?, ?, ?, ?)
                """, (id, text, created_at, author_id, lang))

        logging.info(f"Twitter post collected for keyword: {twitter_keyword}")
        conn.commit()
        conn.close()

    except Exception as e:
        logging.error(f"Error while scraping twitter: {e}")