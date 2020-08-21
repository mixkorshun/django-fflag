from typing import Optional

from ..models import FFlag

pprint_fflag_short_tpl = '{key}; part={part:.2%}; part_ids: {part_ids}'

pprint_fflag_tpl = '''
{key}
 .part:     {part:.2%}
 .part_ids: {part_ids}
'''.strip()


def pprint_fflag(fflag: FFlag) -> Optional[str]:
    return pprint_fflag_tpl.format(
        key=fflag.key + (' [not stored]' if not fflag.id else ''),
        part=fflag.part,
        part_ids=', '.join((str(_id) for _id in fflag.ids)) if len(fflag.ids) else '~',
    )


def pprint_fflag_short(fflag: FFlag) -> Optional[str]:
    return pprint_fflag_short_tpl.format(
        key=fflag.key + (' [not stored]' if not fflag.id else ''),
        part=fflag.part,
        part_ids=','.join((str(_id) for _id in fflag.ids)) if len(fflag.ids) else '~',
    )
