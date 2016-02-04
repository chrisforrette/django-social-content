import json
import urllib2

import dateutil.parser

from django.conf import settings

from .base import BaseSocialContentService


class YoutubeService(BaseSocialContentService):
    """
    Youtube API calls require a google app api key. Make sure you enable the youtube API for your
    google app.

    The content identifier is a playlist ID.
    Youtube groups a channel's uploads into a playlist. This ID will need to be entered in the
    social model. It can be found in the url when clicking on a channel's videos on their uploads
    page.
    """

    social_content_type = 'youtube'
    feed_url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s&key=%s'

    def _fetch(self):
        key = settings.YOUTUBE_APP_API_KEY

        self._raw_payload = urllib2.urlopen(
            self.feed_url % (self.identifier, key)).read()

    def _parse(self):
        decoded = json.loads(self._raw_payload)

        content = []
        for post in decoded['items']:
            simple_status = {
                'post_id': post['id'],
                'message': post['snippet']['title'],
                'timestamp': dateutil.parser.parse(post['snippet']['publishedAt']),  # ISO8601
                'url': 'https://www.youtube.com/watch?v=%s' % post['snippet']['resourceId']['videoId'],
                'image': post['snippet']['thumbnails']['default']['url']
            }
            content.append(simple_status)
        self._parsed_payload = content
