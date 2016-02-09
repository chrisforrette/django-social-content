from django.db import IntegrityError

from social_content.conf import settings
from social_content.models import SocialPost


class BaseSocialContentService(object):
    """Extendable base class for importing data from a social network into db."""
    model = SocialPost

    def __init__(self, identifier, social_account_id):
        self.social_account_id = social_account_id
        self.identifier = identifier

    def get_client(self):
        if not self._client:
            self._client = self._get_client()
        return self._client

    def _get_client(self):
        raise NotImplementedError()

    def import_posts(self):
        """Roll up of all private methods into public data."""
        self._fetch()
        self._parse()
        models = self._create_models()
        self._clean()
        return models

    def _fetch(self):
        """Make API call for data and return raw payload"""
        raise NotImplementedError()

    def _parse(self):
        """Parse payload into simple data."""
        raise NotImplementedError()

    def _clean(self):
        """Clean up the last records"""
        if settings.SOCIAL_CONTENT_MAX_POSTS:
            # Convert to list to prevent mysql from using subquery, which it can't support.
            # NotSupportedError: (1235, "This version of MySQL doesn't yet support 'LIMIT & IN/ALL/ANY/SOME subquery'")
            to_delete = list(self.model.objects.filter(
                social_account_id=self.social_account_id
            ).order_by('-created')[settings.SOCIAL_CONTENT_MAX_POSTS:].values_list(
                'id', flat=True))

            self.model.objects.filter(id__in=to_delete).delete()

    def _create_models(self):
        """Create models from payload."""

        default_attrs = {
            'social_account_id': self.social_account_id,
            'social_content_type': self.social_content_type,
            'payload': self._raw_payload,
        }

        created = 0
        for post in self._parsed_payload:

            attrs = {
                'post_id': post['post_id'],
                'created': post['timestamp'].replace(tzinfo=None),
                'body': post['message'],
                'url': post['url'],
            }

            try:
                attrs['image'] = post['image']
            except KeyError:
                pass

            attrs.update(default_attrs)

            try:
                self.model.objects.create(**attrs)
            except IntegrityError:
                # This post already exists in our database.
                continue
            else:
                created += 1

        return created
