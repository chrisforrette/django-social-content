import logging

from django.conf import settings
from django.db import models

from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel


logger = logging.getLogger(__name__)


STATUS_CHOICES = Choices('active', 'inactive')

SOCIAL_CONTENT_TYPE_CHOICES = tuple((social.lower(), social,) for social in settings.SOCIAL_CONTENT_TYPES)


class SocialAccount(TimeStampedModel, StatusModel):
    """
    Model for social accounts
    """
    STATUS = STATUS_CHOICES

    social_content_type = models.CharField(verbose_name='Type', choices=SOCIAL_CONTENT_TYPE_CHOICES, max_length=255, db_index=True)

    '''
    Identifier for service. Username, handle, etc.

    Twitter: Twitter screen name.

    Facebook: Facebook page ID. This is usually the name after facebook.com/,
    but sometimes the page screen name has not been chosen, and you need to
    use the actual ID in the url.

    Tumblr: Tumblr blog subdomain. aka "example" from "example.tumblr.com".

    Instagram: Instagram username
    '''
    identifier = models.CharField(max_length=255, help_text="""Twitter screenname, Facebook page id, Instagram username,
         or Tumblr subdomain (e.g. "example" from "example.tumblr.com")""")

    raw_identifier = models.CharField(max_length=255, null=True, blank=True)  # The "real", not-necessarily-user-friendly id/entifier

    last_import_error = models.CharField(max_length=255, null=True, blank=True, help_text="""This gets checked when an import runs and fails with the identifier entered here.
        Update your identifier and uncheck this to try and run it again during the next scheduled import""")

    def __unicode__(self):
        return '%s Account (%s)' % (self.get_social_content_type_display(), self.identifier)

    class Meta:
        unique_together = ('social_content_type', 'identifier')
        verbose_name = 'Social Account'

    @property
    def url(self):
        templates = {
            'twitter': 'https://twitter.com/%s',
            'facebook': 'https://www.facebook.com/%s',
            'instagram': 'http://instagram.com/%s',
            'tumblr': 'http://%s.tumblr.com/',
            'spotify': 'https://play.spotify.com/artist/%s',
        }

        return templates[self.social_content_type] % self.identifier

    def fetch_raw_id(self):
        method = 'fetch_%s_raw_id' % self.social_content_type
        if hasattr(SocialAccount, method):
            return getattr(self, method)(self.identifier)
        return None

    @classmethod
    def fetch_instagram_raw_id(cls, identifier):
        client = InstagramAPI(client_id=settings.INSTAGRAM_CLIENT_ID, client_secret=settings.INSTAGRAM_CLIENT_SECRET)
        search = client.user_search(q=identifier)
        if search:
            return search.pop(0).id
        return None

    @classmethod
    def fetch_facebook_raw_id(cls, identifier):
        client = facebook.GraphAPI('%s|%s' % (settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET))
        try:
            search = client.get_object(identifier)
            return search['id']
        except facebook.GraphAPIError:
            raven.captureException(exc_info=sys.exc_info())
            raise

    def set_raw_id(self):
        raw_id = self.fetch_raw_id()
        if raw_id:
            self.raw_identifier = raw_id
        return self.raw_identifier


class SocialPost(TimeStampedModel, StatusModel):
    STATUS = STATUS_CHOICES
    social_account = models.ForeignKey(SocialAccount, related_name='social_posts', blank=True, null=True)

    # This is redundant with the field on SocialAccount, but used for the `unique_together` constraint

    social_content_type = models.CharField(verbose_name='Type', choices=SOCIAL_CONTENT_TYPE_CHOICES, max_length=255, db_index=True)
    payload = models.TextField(blank=True, null=True)  # Raw payload from service.
    post_id = models.CharField(max_length=255)  # Unique ID from service

    # Content fields

    body = models.TextField()
    image = models.TextField() # Image URLs may be longer than 255.
    url = models.CharField(max_length=255) # External URL to post.

    class Meta:
        unique_together = ('social_content_type', 'post_id')
        verbose_name = 'Social Post'
