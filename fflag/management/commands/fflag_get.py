from django.core.management import BaseCommand

from ..pprint import pprint_fflag
from ...models import fflag_get


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('key', type=str)
        parser.add_argument('--with-not-stored', dest='not_stored', action='store_true')

    def handle(self, key, **options):
        fflag = fflag_get(key)
        if not fflag.id and not options.get('not_stored'):
            return

        self.stdout.write(pprint_fflag(fflag))
