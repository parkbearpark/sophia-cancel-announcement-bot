import os

import dotenv
from requests_oauthlib import OAuth1Session


class ManageTwitter:
    def __init__(self):
        consumer_key = os.environ.get('CONSUMER_KEY')
        consumer_secret = os.environ.get('CONSUMER_SECRET')
        access_token = os.environ.get('ACCESS_TOKEN')
        access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

        self.twitter = OAuth1Session(
            consumer_key,
            consumer_secret,
            access_token,
            access_token_secret
        )

    def post_tweet(self, tweet):
        url = "https://api.twitter.com/1.1/statuses/update.json"
        param = {'status': tweet}

        try:
            request = self.twitter.post(url, params=param)
            return True
        except:
            return False
