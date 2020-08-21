from io import StringIO

from django.core.management import call_command

from fflag.models import fflag_set_part


def test_fflag_list_empty():
    output = StringIO()
    call_command('fflag_list', stdout=output)

    assert 'No flags found' in output.getvalue()


def test_fflag_list():
    fflag_set_part('flag1', .955)

    output = StringIO()
    call_command('fflag_list', stdout=output)

    assert 'flag1; part=95.50%; part_ids: ~' in output.getvalue()
