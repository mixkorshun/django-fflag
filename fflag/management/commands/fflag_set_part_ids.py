from django.core.management import BaseCommand

from ..pprint import pprint_fflag
from ...models import fflag_set_part_ids, fflag_get


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('key', type=str)
        parser.add_argument('ids', type=int, nargs='+')

    def handle(self, key, ids, **options):
        fflag_set_part_ids(key, ids)
        fflag = fflag_get(key)
        self.stdout.write(pprint_fflag(fflag))
