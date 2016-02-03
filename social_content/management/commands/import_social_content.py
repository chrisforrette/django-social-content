import logging
import sys
from urllib2 import HTTPError

from django.core.management.base import BaseCommand

from raven.contrib.django.raven_compat.models import client as raven

from epibase.models import Social
from epibase.importers import social_networks


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Iterate over social models and import data with appropriate social import
    class.
    """

    def handle(self, *args, **kwargs):
        for social in Social.objects.active().exclude(has_import_error=True):

            # Initialize correct importer class.
            importer_klass = getattr(social_networks, '%sImport' % social.social_type.capitalize(), None)
            if not importer_klass:
                continue
            importer = importer_klass(social.raw_identifier or social.identifier, social_id=social.pk)

            # Tell importer to do magic.

            try:
                num_models_created = importer.handle()
                logger.info('Created %s %s social posts for id: %s' % (num_models_created, social.social_type, social.identifier,))
            except HTTPError, e:
                logger.error('Social import error for %s account with identifier %s: %s' % (social.social_type, social.identifier, str(e)), exc_info=True)
                raven.captureException(exc_info=sys.exc_info(), extra={'social_type': social.social_type, 'social_identifier': social.identifier})
                social.has_import_error = True
                social.save()
