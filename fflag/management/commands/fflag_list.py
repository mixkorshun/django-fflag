from django.core.management import BaseCommand

from fflag.models import fflag_list, fflag_get
from ..pprint import pprint_fflag_short


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-0', '--only-disabled', action='store_true')
        parser.add_argument('-1', '--only-enabled', action='store_true')

    def handle(self, **options):
        flags = list(fflag_list())

        if not len(flags):
            self.stdout.write('No flags found')
            return

        for flag in flags:
            fflag = fflag_get(flag)

            if options.get('only_disabled') and (fflag.part != 0 or len(fflag.ids) != 0):
                continue

            if options.get('only_enabled') and (fflag.part != 1):
                continue

            self.stdout.write(pprint_fflag_short(fflag))
