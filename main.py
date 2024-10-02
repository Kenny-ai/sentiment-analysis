from textblob import TextBlob
import pandas as pd
import tweepy
import praw
import os


# function for sentimrnt analysis using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return sentiment


# function to get twitter posts
def getTwitterPosts(query):
    consumer_key = "b4jEgL3uMJGk9rEQQVBd9nf1g"
    consumer_secret = "F7JiGuUxuwqwaN1hQRLjwb7goqL0afVGY3S0AhhSqUQjDzSuih"
    access_token = "950421591091015681-XuPlQ3xqEiuV2Je5nJ6GMgc4cNpl6Jd"
    access_token_secret = "VIJ3Jy85WrPSNMCi9hwKfcjcPQF7WH39bJ1GS4BWAJCn0"

    # Pass in our twitter API authentication key
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )

    # Instantiate the tweepy API
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # search_query = "'ref''world cup'-filter:retweets AND -filter:replies AND -filter:links"
    search_query = "'% s'-filter:retweets AND -filter:replies AND -filter:links" % query

    no_of_tweets = 100

    try:
        # The number of tweets we want to retrieved from the search
        tweets = api.search_tweets(
            q=search_query, lang="en", count=no_of_tweets, tweet_mode="extended"
        )

        # Pulling Some attributes from the tweet
        attributes_container = [
            [
                tweet.user.name,
                tweet.created_at,
                tweet.favorite_count,
                tweet.source,
                tweet.full_text,
            ]
            for tweet in tweets
        ]

        # Creation of column list to rename the columns in the dataframe
        columns = [
            "User",
            "Date Created",
            "Number of Likes",
            "Source of Tweet",
            "Tweet",
        ]

        # Analyze sentiment for each post
        for tweet in tweets:
            tweet_text = tweet["full_text"]
            tweet["sentiment"] = analyze_sentiment(tweet_text)

        # Creation of Dataframe
        tweets_df = pd.DataFrame(attributes_container, columns=columns)
        tweets_df.to_excel("twitter-amazon-posts.xlsx", index=False)

    except BaseException as e:
        print("Status failed on", str(e))


# Function to scrape Reddit posts about "Amazon"
def getRedditPosts(query, subreddit="all", limit=100):

    # Initialize PRAW with credentials
    reddit = praw.Reddit(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        user_agent=os.environ["USER_AGENT"],
    )
    posts = []

    try:
        # Search for posts mentioning "Amazon" in the specified subreddit
        for submission in reddit.subreddit(subreddit).search(query, limit=limit):
            posts.append(
                {
                    "body": submission.selftext,
                    "upvotes": submission.score,
                    "url": submission.url,
                }
            )
        # Analyze sentiment for each post
        for post in posts:
            post_text = post["body"]
            post["sentiment"] = analyze_sentiment(post_text)

        # Convert the list of posts to a DataFrame
        df = pd.DataFrame(posts)

        # Export the DataFrame to an Excel file
        df.to_excel("reddit_amazon_posts.xlsx", index=False)

        print("Data exported to reddit_amazon_posts.xlsx")

    except BaseException as e:
        print("Status failed on ", str(e))

    return posts


# Scrape the posts
getRedditPosts("Amazon", limit=60)
# getRedditPosts("Ebay", limit=60)
# getRedditPosts("Etsy", limit=60)
# getRedditPosts("AliExpress", limit=60)
# getRedditPosts("Walmart", limit=60)


getTwitterPosts("amazon")
# ebayTweets = getTwitterPosts("ebay")
# walmartTweets = getTwitterPosts("walmart")
# etsyTweets = getTwitterPosts("etsy")
# aliExpressTweets = getTwitterPosts("aliexpress")
