from io import StringIO

from django.core.management import call_command

from fflag.models import fflag_set_part_ids


def test_fflag_add_part_ids_to_existing():
    fflag_set_part_ids('flag1', [1, 2, 3])

    output = StringIO()
    call_command('fflag_add_part_ids', 'flag1', '4', '5', '6', stdout=output)

    assert 'flag1' in output.getvalue()
    assert '1, 2, 3, 4, 5, 6' in output.getvalue()


def test_fflag_add_part_ids_to_new():
    output = StringIO()
    call_command('fflag_add_part_ids', 'flag1', '4', '5', '6', stdout=output)

    assert 'flag1' in output.getvalue()
    assert '4, 5, 6' in output.getvalue()
