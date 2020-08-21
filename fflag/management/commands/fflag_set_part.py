from django.core.management import BaseCommand

from ..utils import pprint_fflag
from ...models import fflag_set_part


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('key', type=str)
        parser.add_argument('part', type=float)

    def handle(self, key, part, **options):
        fflag_set_part(key, part)
        pprint_fflag(key)
