from django.core.management import BaseCommand

from ..utils import pprint_fflag


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('key', type=str)

    def handle(self, key, **options):
        pprint_fflag(key)
