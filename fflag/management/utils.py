from typing import Sequence

from ..models import fflag_get


def pprint_fflag(key: str):
    fflag = fflag_get(key)

    print(key + '.id:      ', fflag.id)
    print(key + '.part:    ', '%.2f%%' % (fflag.part * 100))
    print(key + '.part_ids:', ', '.join((str(_id) for _id in fflag.ids)) if len(fflag.ids) else '~')


def pprint_fflag_ids(ids: Sequence[int]):
    return ','.join((str(_id) for _id in ids)) if len(ids) else '~'
