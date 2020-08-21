from io import StringIO

from django.core.management import call_command


def test_fflag_set_part():
    output = StringIO()
    call_command('fflag_set_part', 'flag1', '0.825', stdout=output)

    assert 'flag1' in output.getvalue()
    assert '82.50%' in output.getvalue()
