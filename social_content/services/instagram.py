import datetime
import json
import pytz
import urllib2

from django.conf import settings

from .base import BaseSocialContentService


class InstagramService(BaseSocialContentService):
    """Accessing the Instagram API requires an Instgram app client id."""

    social_content_type = 'instagram'
    feed_url = 'https://api.instagram.com/v1/users/%s/media/recent?client_id=%s'

    def _fetch(self):
        client_id = settings.INSTAGRAM_CLIENT_ID

        self._raw_payload = urllib2.urlopen(
            self.feed_url % (self.identifier, client_id)).read()

    def _parse(self):
        decoded = json.loads(self._raw_payload)

        content = []
        for post in decoded['data']:

            # Unix timestamp

            timestamp = datetime.utcfromtimestamp(float(post['created_time'])).replace(tzinfo=pytz.utc)

            simple_status = {
                'post_id': post['id'],
                'timestamp': timestamp,
                'url': post['link'],
                'image': post['images']['standard_resolution']['url']
            }

            simple_status['message'] = post['caption']['text'] if post.get('caption') else ''

            content.append(simple_status)
        self._parsed_payload = content
