import tweepy
from realtime.processor import RealTimeProcessor

class TwitterStreamer(tweepy.StreamingClient):
    def __init__(self, bearer_token, real_time_processor):
        super().__init__(bearer_token)
        self.real_time_processor = real_time_processor

    def on_tweet(self, tweet):
        if tweet.text.startswith("RT @"):
            return
        self.real_time_processor.add_article(tweet.text, f"https://twitter.com/user/status/{tweet.id}")

def start_twitter_stream(bearer_token, real_time_processor):
    stream = TwitterStreamer(bearer_token, real_time_processor)
    stream.add_rules(tweepy.StreamRule("news OR politics"))
    stream.filter()

# Usage:
# processor = RealTimeProcessor()
# processor.start()
# start_twitter_stream('YOUR_BEARER_TOKEN', processor)