import tweepy
import os
from datetime import datetime
from datetime import timezone

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
twitter_account = os.getenv('TWITTER_ACCOUNT')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

intervals = (
    ('m', 2628000),
    ('w', 604800),
    ('d', 86400),
    ('h', 3600),
    ('m', 60),
    ('s', 1),
)

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def getTimeSince(tweetTime):
    tweet_time_utc = int(tweetTime.replace(tzinfo=timezone.utc).timestamp())
    try:
        dt = datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()
        utc_time_now = int(utc_timestamp)
        tweetTimeSince = f"{display_time(abs(utc_time_now - tweet_time_utc), 2)}"
    except Exception as e:
        tweetTimeSince = ''
        print("time since error", e)
    return tweetTimeSince

def get_last_tweets(id):
    tweet_list = api.user_timeline(id=id, count=50, tweet_mode='extended')
    fav_list = []
    ret_list = []
    url_list = []
    time_list = []
    for tweet in tweet_list:
        if tweet.in_reply_to_status_id is not None:
            # Tweet is a reply
            is_reply = True
        else:
            # Tweet is not a reply
            is_reply = False

        if not tweet.retweeted and not is_reply:
            # print(tweet)
            time_list.append(getTimeSince(tweet.created_at))
            fav_list.append(tweet.favorite_count)
            ret_list.append(tweet.retweet_count)
            url_list.append(f"https://twitter.com/{twitter_account}/status/{tweet.id}")
            if len(url_list) == 10:
                return fav_list, ret_list, url_list, time_list
    return fav_list, ret_list, url_list, time_list

def arrangeTweets(fav_list, ret_list, url_list, time_list):
    text = ''
    for i in range(len(url_list)):
        text = text + f"❤{fav_list[i]} • 🔁{ret_list[i]} • {time_list[i]} • [🐦Tweet]({url_list[i]})\n"
    return text


def getTweetsText():
    if api.verify_credentials():
        # myId = api.me().id
        myId = os.getenv('MY_TWITTER_ID')
        allTweetText = ''
        try:
            fav_list, ret_list, url_list, time_list = get_last_tweets(myId)
            allTweetText = arrangeTweets(fav_list, ret_list, url_list, time_list)
            return allTweetText
        except Exception as e:
            print("ERROR GETTING TWEET ", e)
        return allTweetText
    else:
        print("API not Connected")
        return None

#print(getTweetsText())