from io import StringIO

from django.core.management import call_command

from fflag.models import fflag_set_part


def test_fflag_get_existing():
    fflag_set_part('flag1', .955)

    output = StringIO()
    call_command('fflag_get', 'flag1', stdout=output)

    assert 'flag1' in output.getvalue()
    assert '95.50%' in output.getvalue()


def test_fflag_get_unexisting():
    output = StringIO()
    call_command('fflag_get', 'flag1', stdout=output)

    assert 'flag1' not in output.getvalue()


def test_fflag_get_unexisting_with_with_not_stored_opt():
    output = StringIO()
    call_command('fflag_get', 'flag1', '--with-not-stored', stdout=output)

    assert 'flag1' in output.getvalue()
    assert '[not stored]' in output.getvalue()
    assert '0.00%' in output.getvalue()
