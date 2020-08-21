from django.core.management import BaseCommand

from fflag.models import fflag_list, fflag_get
from ..utils import pprint_fflag_ids


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-0', '--only-disabled', action='store_true')
        parser.add_argument('-1', '--only-enabled', action='store_true')

    def handle(self, **options):
        flags = fflag_list()
        if not flags:
            print('No flags found')
            return

        for flag in flags:
            fflag = fflag_get(flag)

            if options.get('only_disabled') and (fflag.part != 0 or len(fflag.ids) != 0):
                continue

            if options.get('only_enabled') and (fflag.part != 1):
                continue

            print(fflag.key + ';', 'part=%s;' % fflag.part, 'part_ids=%s' % pprint_fflag_ids(fflag.ids))
