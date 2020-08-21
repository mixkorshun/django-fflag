from django.core.management import BaseCommand

from fflag.models import fflag_list, fflag_enabled


class Command(BaseCommand):
    help = "prints feature flags for specified id"

    def add_arguments(self, parser):
        parser.add_argument('-a', '--show-all', action='store_true')
        parser.add_argument('id')

    def handle(self, id, **options):
        id = int(id)
        show_all = options.get('show_all')
        for flag in fflag_list():
            if fflag_enabled(id, flag):
                print('+%s' % flag if show_all else flag)
            elif show_all:
                print('-%s' % flag)
