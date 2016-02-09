from django.core.management.base import BaseCommand

from social_content.tasks import import_social_content


class Command(BaseCommand):
    """
    Iterate over social models and import post data with appropriate social import
    class.
    """
    def add_arguments(self, parser):
        parser.add_argument(
            '--async',
            dest='async',
            default=False,
            action='store_true',
            help='Run this command asynchronously on a Celery worker (if you have it installed)'
        )

    def handle(self, **options):
        async = options.get('async')

        if async and hasattr(import_social_content, 'delay'):
            import_social_content.delay()
        else:
            import_social_content()
