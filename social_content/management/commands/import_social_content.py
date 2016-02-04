from django.core.management.base import BaseCommand

from social_content.tasks import import_social_content


class Command(BaseCommand):
    """
    Iterate over social models and import post data with appropriate social import
    class.
    """

    def handle(self, *args, **kwargs):
        import_social_content()
