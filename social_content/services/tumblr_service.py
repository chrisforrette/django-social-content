import datetime
import json
import urllib2

import pytz

from social_content.conf import settings

from .base import BaseSocialContentService


class TumblrService(BaseSocialContentService):
    """Accessing the Tumblr endpoint requires a Tumblr app consumer key."""

    social_content_type = 'tumblr'
    feed_url = 'http://api.tumblr.com/v2/blog/%s.tumblr.com/posts?api_key=%s'

    def _fetch(self):
        api_key = settings.TUMBLR_API_CONSUMER_KEY

        self._raw_payload = urllib2.urlopen(
            self.feed_url % (self.identifier, api_key)).read()

    def _parse(self):
        decoded = json.loads(self._raw_payload)

        content = []
        for post in decoded['response']['posts']:

            # Assuming we only want text or photo posts.

            if post['type'] not in ['text', 'photo']:
                continue

            # Unix timestamp

            timestamp = datetime.utcfromtimestamp(post['timestamp']).replace(tzinfo=pytz.utc)

            simple_status = {
                'post_id': post['id'],
                'message': post.get('body') or post.get('caption'),
                'timestamp': timestamp,
                'url': post['post_url'],
            }

            if post['type'] == 'photo':
                simple_status['image'] = post['photos'][0]['alt_sizes'][0]['url']

            content.append(simple_status)
        self._parsed_payload = content
