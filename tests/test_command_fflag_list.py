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


def test_fflag_list_only_disabled():
    fflag_set_part('flag1', 1)
    fflag_set_part('flag2', 0)
    fflag_set_part('flag3', 0.5)

    output = StringIO()
    call_command('fflag_list', '-0', stdout=output)

    assert 'flag1' not in output.getvalue()
    assert 'flag2' in output.getvalue()
    assert 'flag3' not in output.getvalue()


def test_fflag_list_only_enabled():
    fflag_set_part('flag1', 1)
    fflag_set_part('flag2', 0)
    fflag_set_part('flag3', 0.5)

    output = StringIO()
    call_command('fflag_list', '-1', stdout=output)

    assert 'flag1' in output.getvalue()
    assert 'flag2' not in output.getvalue()
    assert 'flag3' not in output.getvalue()
