import json
import urllib2

import dateutil.parser

from django.conf import settings

from .base import BaseSocialContentService


class FacebookService(BaseSocialContentService):
    """Accessing Facebook page public feeds requires a facebook 'app_id' and 'app_secret'."""

    social_content_type = 'facebook'
    graph_url = 'https://graph.facebook.com/%s/posts?access_token=%s|%s'

    def _fetch(self):
        app_id = settings.FACEBOOK_APP_ID
        app_secret = settings.FACEBOOK_APP_SECRET

        self._raw_payload = urllib2.urlopen(
            self.graph_url % (self.identifier, app_id, app_secret)).read()

    def _parse(self):
        decoded = json.loads(self._raw_payload)

        content = []
        for post in decoded['data']:

            # Assuming we only want actual status updates since we're aggregating other sources.
            if post['type'] != 'status' or not post.get('message'):
                continue

            simple_status = {
                'post_id': post['id'],
                'message': post['message'],
                'timestamp': dateutil.parser.parse(post['created_time']),  # ISO8601
                'url': 'https://www.facebook.com/%s/posts/%s' % (
                    post['id'].split('_')[0], post['id'].split('_')[1]
                ),
            }
            content.append(simple_status)
        self._parsed_payload = content
