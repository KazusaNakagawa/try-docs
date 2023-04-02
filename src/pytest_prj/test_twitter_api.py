import sys

import requests_mock
import unittest
from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock
from models.twitter_api import TwitterAPI

sys.modules['controller.api.slack'] = Mock()


# テスト対象の関数
@patch('models.twitter_api.TwitterAPI')
def test_gpt(mock_twitter_api):
    twitter_api = TwitterAPI(mock_twitter_api)
    assert twitter_api.get_keyword() == "GPT"


# TwitterAPIをモック化するテスト
@patch('models.twitter_api.TwitterAPI')
def test_gpt_with_mock(mock_twitter_api):
    # TwitterAPIのsearchメソッドが返す値を設定
    mock_twitter_api.return_value.search.return_value = [
        {'text': 'I love GPT', 'created_at': '2022-01-01 12:00:00'}
    ]
    twitter_api = TwitterAPI('mock_api')
    assert twitter_api.get_keyword() == "GPT"


class TestTwitterAPI(TestCase):
    """twitter.TwitterをMockしています。
    # FIXME: Test did not pass.

    mock_twitter_instanceのsearchプロパティをPropertyMockに設定し、[mocked_tweet]を返すようにしています。
    次に、mock_twitterを使用して、mock_twitter_instanceを返すように設定し、get_tweets_with_keyword関数を呼び出しています。
    最後に、期待されるツイートと実際に取得されたツイートを比較しています。
    """
    @patch('models.twitter_api.TwitterAPI')
    def test_get_tweets_with_gpt_keyword(self, mock_twitter):
        # Mocked tweet response
        mocked_tweet = {
            'created_at': 'Tue Apr 20 21:00:00 +0000 2021',
            'id': 1384581400380590082,
            'text': 'Just learned about GPT from @OpenAI. Amazing stuff!',
            'user': {
                'id': 123456,
                'screen_name': 'test_user'
            }
        }

        # Mock the response from the Twitter API
        mock_twitter_instance = Mock()
        type(mock_twitter_instance).search = PropertyMock(return_value=[mocked_tweet])
        mock_twitter.return_value = mock_twitter_instance

        # Call the function that uses the Twitter API
        twitter_api = TwitterAPI(mock_twitter)
        tweets = twitter_api.search('GPT', num_tweets=1)

        # Assert that the function returns the expected tweets
        expected_tweets = [
            {
                'created_at': 'Tue Apr 20 21:00:00 +0000 2021',
                'id': 1384581400380590082,
                'text': 'Just learned about GPT from @OpenAI. Amazing stuff!',
                'user': {
                    'id': 123456,
                    'screen_name': 'test_user'
                }
            }
        ]
        self.assertEqual(tweets, expected_tweets)
