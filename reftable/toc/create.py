# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import re

import configo
import elements
import iamraw
import utila

import reftable.toc

APPENDIX_LEVEL = configo.HV_INT_PLUS(default=100)


def groupby_chapter(items: reftable.toc.TocLines):
    """Group by chapter."""
    # TODO: DONT KNOW WHY WE NEED THIS?
    assert isinstance(items, list), type(items)
    for item in items:
        assert isinstance(item, reftable.toc.TocLine), type(item)
    result = []
    collected = []
    for item in items:
        if item.level is None:
            if collected:
                result.append(collected)
                collected = []
            result.append([item])
            continue
        if collected and collected[-1].level[0] != item.level[0]:
            result.append(collected)
            collected = [item]
        else:
            collected.append(item)
    if collected:
        result.append(collected)
    return result


@dataclasses.dataclass
class Level:
    # TODO: MOVE TO IAMRAW
    value: int = None
    raw: str = dataclasses.field(compare=False, default=None)

    def __int__(self):
        return self.value


class RomanLevel(Level):
    pass


class StepLevel(Level):
    pass


class SectionsLevel(Level):
    pass


@dataclasses.dataclass
class AppendixLevel(Level):
    """\
    Example::
        A.1.1
    """
    character: str = None

    def __int__(self):
        return APPENDIX_LEVEL


def level(item: str) -> Level:
    """Determine level out of parsed level string.

    Examples:
      - IV Anhang
      - 4.1.1 Datenschicht
      - 5 Implementierung
      - None Literaturverzeichnis

    >>> level('A')
    AppendixLevel(value='A', raw='A', character='A')
    >>> level('b')
    AppendixLevel(value='B', raw='b', character='B')
    >>> level('4.')
    Level(value=1, raw='4.')
    >>> level('A.')
    Level(value=1, raw='A.')
    >>> level('A.1.1')
    Level(value=3, raw='A.1.1')
    >>> level('A.1.')
    Level(value=2, raw='A.1.')
    """
    # TODO: SUPPORT 1. Abbildung
    # TODO: SUPPORT 1. Abb.
    # In the current implementation there are valid cause of 'A' in Abb/
    # Abbildung, but this is not the correct Point.
    if item is None:
        return None
    number = elements.level_numbered(item)
    if number is not None:
        return Level(value=number, raw=item)
    if value := utila.arabic(item):
        return RomanLevel(value=value, raw=item)
    try:
        letter, _ = item.split('.', maxsplit=1)
        letter = letter.upper()
    except ValueError:
        # TODO: REMOVE THIS HACK AFTER FIXING LINEREGEX
        letter = item.replace('Anhang', '').replace(':', '').strip().upper()
    if letter in 'ABCDEFGH':
        result = AppendixLevel(value=letter, character=letter, raw=item)
        return result
    if converted := elements.level_steps(item):
        result = StepLevel(value=converted, raw=item)  # pylint:disable=R0204
        return result
    utila.error(f'could not convert to level: {item}')
    return None


# TODO: MOVE TO ELEMENTS
def groupby_level(toc: reftable.toc.TocLines) -> iamraw.Toc:
    if not toc:
        # empty toc or no toc
        return iamraw.Toc()
    style = elements.toc_style(toc)
    if style == iamraw.TocStyle.NUMBERED:
        return groupby_level_numbered(toc)
    if style == iamraw.TocStyle.SECTIONED:
        return grouper_level(toc, levelme=level_sections, style=style)
    if style == iamraw.TocStyle.FIRSTLEVEL_ONLY:
        # TODO: VERIFY THIS
        return grouper_level(
            toc,
            levelme=lambda x: 1 if x is not None else 2,
            style=style,
        )
    assert style == iamraw.TocStyle.STEPPED, str(style)
    result = groupby_level_steps(toc)
    return result


def groupby_level_numbered(toc: reftable.toc.TocLines) -> iamraw.Toc:
    return grouper_level(
        toc,
        levelme=determine_level,
        style=iamraw.TocStyle.NUMBERED,
    )


def groupby_level_steps(toc: reftable.toc.TocLines) -> iamraw.Toc:
    """\
    Example
        A Lateinische Buchstaben
            I. Roman numbers
                1. Arabische Zahlen
                    a. Lateinische Kleinbuchstaben
    """
    return grouper_level(
        toc,
        levelme=elements.level_steps,
        style=iamraw.TocStyle.STEPPED,
    )


def grouper_level(
    toc: reftable.toc.TocLines,
    levelme=None,
    style: iamraw.TocStyle = None,
) -> iamraw.Toc:
    """Create `iamraw.Toc` out of list of `reftable.toc.TocLine`

    Determine level of toc line and replace it with determined int-level.

    Args:
        toc: extracted table of content.
        levelme(callable): convert raw to int level
        style(TocStyle): toc style
    Returns:
        Table of content with replaced levels.
    """
    assert isinstance(toc, list), type(toc)
    if levelme is None:
        levelme = determine_level
    outlines = []
    for line in toc:
        if not line:
            utila.error(f'problem while processing lines: {line}')
            continue
        if not isinstance(line, reftable.toc.TocLine):
            continue
        levels = levelme(line.level)
        section = iamraw.SectionRaw(
            level=levels,
            page=line.page,
            title=line.title,
            raw=line.raw,
            raw_location=line.pdfpage,
            raw_level=line.level,
        )
        outlines.append(section)
    outlines = level_zero(outlines)
    result = iamraw.create_toc(outlines, style=style)
    return result


def level_zero(items):
    """Ensure that no toc has level zero

    Problem:
        1 Einleitung
        1.1 Aufbau der Arbeit
        update every level to ensure
    """
    # TODO: REMOVE THIS?
    level_min = min(
        [item.level for item in items if item.level is not None],
        default=utila.INF,
    )
    if not level_min:
        for item in items:
            item.level = item.level + 1
    return items


def determine_level(levels) -> int:
    if levels is None:
        return 1
    numbered = elements.level_numbered(levels)
    if numbered is None:
        return 1
    return numbered


@utila.cacheme
def level_sections(raw: str) -> int:  # pylint:disable=R0911
    """Convert number to raw level.

    Example:

        Section 3: Data
        Section 4: Methodology
        Section 5: Results
            Part 1: Time series analysis
            Part 2: Looking for pair-wise cointegration
                Cointegrating pairs

    >>> level_sections('Section 1: Introduction')
    1
    >>> level_sections('Part 3:Was ist Sicherheit?')
    2
    >>> level_sections('Umwelt und Klimawandel')
    3
    """
    # TODO: MOVE TO ELEMENTS
    raw = raw.strip() if raw else None
    if not raw:
        return 3
    if re.match(r'^(SECTION)[ ]{1,3}\d{1,2}\:', raw, re.IGNORECASE):
        return 1
    if re.match(r'^(Part)[ ]{1,3}\d{1,2}\:', raw, re.IGNORECASE):
        return 2
    return 3


def istocsections(toc) -> bool:
    """Decide if a toc contains headlines with numbered or steps pattern."""
    if not toc:
        return True
    levels = len([
        item for item in toc
        if item.level and level_sections(item.level) in (1, 2)
    ])
    rate = levels / len(toc)
    if rate < 0.65:  # TODO: HOLY VALUE
        return False
    return True


def istocnolevel(toc) -> bool:
    if not toc:
        return True
    levels = len([item for item in toc if item.level is None])
    rate = levels / len(toc)
    if rate < 0.65:  # TODO: HOLY VALUE
        return False
    return True
