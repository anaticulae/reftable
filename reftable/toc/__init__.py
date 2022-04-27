# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import typing

import utila


@dataclasses.dataclass
class TocLine:
    level: str = None
    title: str = None
    page: str = None
    raw: str = dataclasses.field(default=None, compare=False)
    raw_location: str = dataclasses.field(default=None, compare=False)
    raw_level: str = dataclasses.field(default=None, compare=False)


TocLines = typing.List[TocLine]


def remove_duplication(headlines: TocLines) -> TocLines:
    """Remove duplications out of list of headlines."""
    result = []
    inserted = set()
    for item in headlines:
        if item.title in inserted:
            continue
        result.append(item)
        inserted.add(item.title)
    return result


def sort_byposition(lines: TocLines, content: str) -> TocLines:
    position = {}
    for item in lines:
        # search by raw to avoid finding subpattern
        pos = content.find(item.raw)
        # ensure to avoid finding duplicated items twice
        content = whitespace(content, item.raw)
        position[pos] = item
    result = [position[item] for item in sorted(position.keys())]
    return result


def whitespace(content, pattern):
    """Replace `pattern` with whitespace and avoid removing newlines."""
    replacement = ''.join([
        ' ' if item is not utila.NEWLINE else utila.NEWLINE for item in pattern
    ])
    result = content.replace(pattern, replacement)
    return result
