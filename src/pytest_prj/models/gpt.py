from typing import List


class GPT:
    def __init__(self, twitter_api):
        self.twitter_api = twitter_api

    def get_keyword(self) -> str:
        return "GPT"

    def get_tweets_with_keyword(self, keyword: str, num_tweets=20) -> List[dict]:
        tweets = []
        response = self.twitter_api.search(q=keyword, lang='en', result_type='recent', count=num_tweets)
        for tweet in response['statuses']:
            tweets.append({
                'created_at': tweet['created_at'],
                'id': tweet['id'],
                'text': tweet['text'],
                'user': {
                    'id': tweet['user']['id'],
                    'screen_name': tweet['user']['screen_name']
                }
            })
        return tweets
