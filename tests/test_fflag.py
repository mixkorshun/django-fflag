import random
import string

import pytest
from django.core.cache import caches

from fflag.models import fflag_get, fflag_delete, fflag_rearrange, fflag_set_part, fflag_enabled


def _randstr(n):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


def setup_function(function):
    caches['default'].clear()


def test_fflag_disabled_by_default():
    flag = _randstr(8)

    for i in range(100, 200):
        assert not fflag_enabled(i, flag)


def test_fflag_auto_create_on_check():
    flag = _randstr(8)
    fflag_enabled(1, flag)

    fflag = fflag_get(flag)

    assert fflag.id > 0

    assert fflag.part == 0
    assert len(fflag.ids) == 0


def test_fflag_rearrange():
    fflag_set_part('flag1', 1)
    fflag_set_part('flag2', 1)
    fflag_set_part('flag5', 1)
    fflag_set_part('flag4', 1)
    fflag_set_part('flag3', 1)

    assert fflag_get('flag5').id == 3
    assert fflag_get('flag4').id == 4
    assert fflag_get('flag3').id == 5
    assert caches['default'].get('fflag_max_id') == 5

    fflag_delete('flag1')
    fflag_delete('flag2')

    fflag_rearrange()

    assert fflag_get('flag5').id == 1
    assert fflag_get('flag4').id == 2
    assert fflag_get('flag3').id == 3

    assert caches['default'].get('fflag_max_id') == 3


@pytest.mark.longrun
@pytest.mark.parametrize("key", [_randstr(8), _randstr(10)])
def test_fflag_enabled_for_all(key):
    fflag_set_part(key, 1)

    for i in range(1000, 2000):
        assert fflag_enabled(i, key)


@pytest.mark.longrun
@pytest.mark.parametrize("key", [_randstr(8), _randstr(10)])
def test_fflag_disabled_for_all(key):
    fflag_set_part(key, 0)

    for i in range(1000, 2000):
        assert not fflag_enabled(i, key)


@pytest.mark.longrun
@pytest.mark.parametrize("key", [_randstr(8), _randstr(10)], ids=lambda x: 'str%s' % len(x))
@pytest.mark.parametrize("part", [.27, .50])
@pytest.mark.parametrize("k", [1, 2, 3])
def test_fflag_partially_enabled(key, part, k):
    fflag_set_part(key, part)

    yes = 0
    for i in range(0, 100000, k):
        yes += 1 if fflag_enabled(i, key) else 0

    assert (yes / 100000) - part < .0001
