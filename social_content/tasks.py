import logging
from urllib2 import HTTPError

from .models import SocialAccount
from .utils import get_service_class_by_name, ServiceDoesNotExist


logger = logging.getLogger(__name__)


def import_social_content():
    """
    Iterate over all active social accounts and import post data with matching
    social service class.
    """
    for social_account in SocialAccount.active.all():
        try:
            service = get_service_class_by_name(social_account.social_content_type)
        except ServiceDoesNotExist, e:
            logger.error(str(e), exc_info=True)
            continue

        importer = service(social_account.raw_identifier or social_account.identifier, social_account_id=social_account.pk)

        # Tell importer to do magic.

        try:
            num_models_created = importer.import_posts()
            logger.info('Created %s %s social posts for id: %s' % (num_models_created, social_account.social_content_type, social_account.identifier,))
        except HTTPError, e:
            logger.error('Social import error for %s account with identifier %s: %s' % (social_account.social_content_type, social_account.identifier, str(e)), exc_info=True)

            # If error, deactivate the account and store the error message

            social_account.status = SocialAccount.STATUS.inactive
            social_account.last_import_error = str(e)
            social_account.save()
