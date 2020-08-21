from dataclasses import dataclass
from functools import reduce
from math import log10, floor
from typing import Sequence

from django.conf import settings
from django.core.cache import caches, BaseCache

from fflag import default_settings


@dataclass
class FFlag:
    id: int
    key: str
    part: float
    ids: Sequence[int]

    def __str__(self):
        return self.key

    def __repr__(self):
        return 'FFlag<%s>' % self.key


def __fflag_new(flag: str):
    cache: BaseCache = caches[getattr(settings, 'FFLAG_CACHE_NAME', default_settings.FFLAG_CACHE_NAME)]

    try:
        fflag_id = cache.incr('fflag_max_id')
    except ValueError:
        cache.add('fflag_max_id', 0)
        fflag_id = cache.incr('fflag_max_id')

    cache.set('fflag_id_%s' % fflag_id, flag, None)
    cache.set('fflag_%s/id' % flag, fflag_id, None)

    return fflag_id


def __fflag_read(flag: str, auto_create=True) -> FFlag:
    cache: BaseCache = caches[getattr(settings, 'FFLAG_CACHE_NAME', default_settings.FFLAG_CACHE_NAME)]
    values = cache.get_many((
        'fflag_%s/id' % flag,
        'fflag_%s/part' % flag,
        'fflag_%s/ids' % flag,
    ))

    flag_id = values.get('fflag_%s/id' % flag)
    if not flag_id and auto_create:
        flag_id = __fflag_new(flag)

    return FFlag(
        id=flag_id,
        key=flag,
        part=values.get('fflag_%s/part' % flag, 0),
        ids=values.get('fflag_%s/ids' % flag, ()),
    )


def __fflag_write(fflag: FFlag, attrs=()):
    cache: BaseCache = caches[getattr(settings, 'FFLAG_CACHE_NAME', default_settings.FFLAG_CACHE_NAME)]

    if not fflag.id:
        fflag.id = __fflag_new(fflag.key)

    data = {}
    attrs = set(attrs).intersection(('part', 'ids'))
    for attr in attrs:
        data['fflag_%s/%s' % (fflag.key, attr)] = getattr(fflag, attr)

    cache.set_many(data, None)


def __fflag_delete(fflag: FFlag):
    cache: BaseCache = caches[getattr(settings, 'FFLAG_CACHE_NAME', default_settings.FFLAG_CACHE_NAME)]

    cache.delete_many((
        'fflag_id_%s' % fflag.id,

        'fflag_%s/id' % fflag.key,
        'fflag_%s/part' % fflag.key,
        'fflag_%s/ids' % fflag.key,
    ))

    cache.delete('fflag_%s/__MUTEX__' % fflag.key)


def fflag_list():
    cache: BaseCache = caches[getattr(settings, 'FFLAG_CACHE_NAME', default_settings.FFLAG_CACHE_NAME)]
    fflag_max_id = cache.get('fflag_max_id', 0)

    if fflag_max_id:
        cache_values = cache.get_many([
            'fflag_id_%s' % flag_id
            for flag_id in range(1, fflag_max_id + 1)
        ])

        for flag_id in range(1, fflag_max_id + 1):
            cache_key = 'fflag_id_%s' % flag_id
            flag = cache_values.get(cache_key)
            if not flag:
                continue

            yield flag


def fflag_rearrange():
    cache: BaseCache = caches[getattr(settings, 'FFLAG_CACHE_NAME', default_settings.FFLAG_CACHE_NAME)]
    fflag_max_id = cache.get('fflag_max_id', 0)

    if not fflag_max_id:
        return

    cache_values = cache.get_many([
        'fflag_id_%s' % flag_id
        for flag_id in range(1, fflag_max_id + 1)
    ])

    flags = []

    for flag_id in range(1, fflag_max_id + 1):
        cache_key = 'fflag_id_%s' % flag_id
        flag = cache_values.get(cache_key)
        if not flag:
            continue

        flags.append(flag)

    fflag_new_max_id = len(flags)

    cache.set_many({
        'fflag_max_id': fflag_new_max_id,
        **({'fflag_%s/id' % flag: i for i, flag in enumerate(flags, 1)}),
        **({'fflag_id_%s' % i: flag for i, flag in enumerate(flags, 1)}),
    }, None)

    cache.delete_many(['fflag_id_%s' % i for i in range(fflag_new_max_id, fflag_max_id)])


def fflag_get(flag: str) -> FFlag:
    return __fflag_read(flag, auto_create=False)


def fflag_set_part(flag: str, part: float):
    assert 0 <= part <= 1, '0 <= [part] <= 1'
    precision = floor(log10(1 / getattr(settings, 'FFLAG_PRECISION', default_settings.FFLAG_PRECISION)))

    fflag = __fflag_read(flag)
    fflag.part = round(part, precision)
    __fflag_write(fflag, ('part',))


def fflag_add_part_ids(flag: str, ids: Sequence[int]):
    fflag = __fflag_read(flag)
    fflag.ids = tuple(fflag.ids) + tuple(ids)
    __fflag_write(fflag, ('ids',))


def fflag_set_part_ids(flag: str, ids: Sequence[int]):
    fflag = __fflag_read(flag)
    fflag.ids = ids
    __fflag_write(fflag, ('ids',))


def fflag_delete(flag: str):
    fflag = __fflag_read(flag)
    __fflag_delete(fflag)


def fflag_enabled(_id: int, flag: str) -> bool:
    fflag = __fflag_read(flag)

    if _id in fflag.ids:
        return True

    if fflag.part == 0:
        return False
    elif fflag.part == 1:
        return True

    m = floor(1 / getattr(settings, 'FFLAG_PRECISION', default_settings.FFLAG_PRECISION))

    uniq_value = reduce(lambda p, c: _lcg(p + ord(c), m), flag, 0)
    uniq_value = _lcg(uniq_value + _id, m)
    return uniq_value < fflag.part * m


def _lcg(x: int, m: int) -> int:
    """
    Linear congruential generator
    """
    a, c = getattr(settings, 'FFLAG_LCG_AC', default_settings.FFLAG_LCG_AC)

    return (a * x + c) % m
