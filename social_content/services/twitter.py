import dateutil.parser
import json
import urllib2

from django.conf import settings

from .base import BaseSocialContentService


class TwitterService(BaseSocialContentService):
    """
    Accessing Twitter feeds requires an app 'bearer_token'.

    Easy way to get a bearer token given an app's consumer keys...

    request = urllib2.Request("https://api.twitter.com/oauth2/token",
        'grant_type=client_credentials',
        headers={"Authorization" : "Basic %s" % b64encode('(api key):(api secret)'),
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"})
    urllib2.urlopen(request).read()
    """

    social_content_type = 'twitter'
    timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?exclude_replies=true&screen_name=%s'

    def _fetch(self):
        """Does not include replies."""
        headers = {'Authorization': 'Bearer %s' % settings.TWITTER_BEARER_TOKEN}
        request = urllib2.Request(self.timeline_url % self.identifier, headers=headers)
        self._raw_payload = urllib2.urlopen(request).read()

    def _parse(self):
        decoded = json.loads(self._raw_payload)

        content = []
        for post in decoded:

            # Assuming we don't want retweets.
            if post.get('retweeted_status') or post['text'][0:2] == 'RT':
                continue

            simple_status = {
                'post_id': post['id_str'],
                'message': post['text'],
                'timestamp': dateutil.parser.parse(post['created_at']),  # ISO8601
                'url': 'https://twitter.com/%s/status/%s' % (self.identifier, post['id']),
            }
            content.append(simple_status)
        self._parsed_payload = content
