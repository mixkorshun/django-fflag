from django.core.management import BaseCommand

from ..utils import pprint_fflag
from ...models import fflag_add_part_ids


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('key', type=str)
        parser.add_argument('ids', type=int, nargs='+')

    def handle(self, key, ids, **options):
        fflag_add_part_ids(key, ids)
        pprint_fflag(key)
