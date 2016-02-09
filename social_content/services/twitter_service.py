import json
import urllib2

import dateutil.parser

import twitter

from social_content.conf import settings

from .base import BaseSocialContentService


class Service(BaseSocialContentService):
    """
    Twitter service, requires the following settings: TWITTER_CONSUMER_KEY, 
    TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET
    """

    social_content_type = 'twitter'

    def _get_client(self):
        return twitter.Api(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
        )

    def _fetch(self):
        """Does not include replies."""
        client = self._get_client()
        self._raw_payload = map(lambda tweet: tweet.AsDict(), client.GetUserTimeline(screen_name=self.identifier))

    def _parse(self):
        content = []

        for post in self._raw_payload:

            # Assuming we don't want retweets.
            if post.get('retweeted_status') or post['text'][0:2] == 'RT':
                continue

            simple_status = {
                'post_id': str(post['id']),
                'message': post['text'],
                'timestamp': dateutil.parser.parse(post['created_at']),  # ISO8601
                'url': 'https://twitter.com/%s/status/%s' % (self.identifier, post['id']),
            }
            content.append(simple_status)
        self._parsed_payload = content
