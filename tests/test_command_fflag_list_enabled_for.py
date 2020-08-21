from io import StringIO

from django.core.management import call_command

from fflag.models import fflag_set_part


def test_command_fflag_list_enabled_for():
    fflag_set_part('flag1', 1)
    fflag_set_part('flag2', 0)
    fflag_set_part('flag3', 1)

    output = StringIO()
    call_command('fflag_list_enabled_for', '1', stdout=output)

    assert 'flag1' in output.getvalue()
    assert 'flag2' not in output.getvalue()
    assert 'flag3' in output.getvalue()


def test_command_fflag_list_enabled_for_show_all():
    fflag_set_part('flag1', 1)
    fflag_set_part('flag2', 0)
    fflag_set_part('flag3', 1)

    output = StringIO()
    call_command('fflag_list_enabled_for', '1', '--show-all', stdout=output)

    assert '+flag1' in output.getvalue()
    assert '-flag2' in output.getvalue()
    assert '+flag3' in output.getvalue()
