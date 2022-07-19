# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import re

import elements
import utila

import reftable.toc


@utila.cacheme
def parse(line: str) -> reftable.toc.TocLine:
    """\
    >>> parse('5. Initiative: ´Demenzfreundliche Kommune`................. 45')
    TocLine(level='5.', title='Initiative: ´Demenzfreundliche Kommune`', page='45'...')
    >>> parse('3.1.4 MOBILITÄTSKONZEPT NÖ 2030+  63')
    TocLine(level='3.1.4', title='MOBILITÄTSKONZEPT NÖ 2030+'...)
    >>> parse('4.5.1 Charakteristisches Schwingungsverhalten der OH*-Intensität und der CoLE- Position . . . 74')
    TocLine(level='4.5.1', title='Charakteristisches...Position', page='74'...)
    """
    assert isinstance(line, str), type(line)
    # see bachelor128
    # 8.1         Fazit.................. 87
    line = utila.normalize_whitespaces(line)
    for pattern in [
            EXTENDED_PATTERN_LETTER,
            EXTENDED_PATTERN,
            NO_DOTS,
            NO_LEVEL,
            DICTIONARY,
    ]:
        matched = re.match(pattern, line)
        if not matched:
            continue
        return extract_match(matched)
    return None


def parse_linestart(line: str) -> reftable.toc.TocLine:
    """\
    >>> parse_linestart('5. Initiative: ´Demenzfreundliche Kommune`................. ')
    TocLine(...title='Initiative:...)
    """
    matched = LINESTART.match(line)
    if not matched:
        return None
    result = extract_match(matched)
    result.raw = line
    result.title = line[line.index(result.title):]
    return result


LEVEL_DOTTED_OPTIONAL = r'(?P<level>(\d{1,2}\.?){1,3}\d{0,2})'

LEVEL_LETTER = r"""
    (?P<level>
        (
            (A|B|C|D|E|F|G)(
                \.(\d{1,2}\.?)+\d{0,2}|
                [\.\)]|
                # empty is also fine
            )
            |
            (AA|BB|CC|DD|EE|FF|GG)\)|
            (III|II|I|IV|VIIII|VIII|VII|VI|V|IX|XIII|XII|XI|X)
            (
                \.\d{0,1} # IV or optional number:  IV.2
                |
                \)        # IV)
            )
            |
            (KAPITEL|CHAPTER)[ ]\d{1,2}|
            (SECTION|PART)[ ]{0,3}\d{1,2}:|
            (ANHANG|APPENDIX)[ ](A|B|C|D)\:| # TODO: Exclude Anhang and :
            \(\d{1,2}\)
        )
    )
"""

USER_CHARACTER = [
    r'\w\d\(\)\-\.\[\]\+',
    "'!\"&,/:;?ß*#",
    '’‚“”„…',
    '´`',
    '–',  # special minus sign
]

UC_NWS = ''.join(USER_CHARACTER)
UC = UC_NWS + ' '  # user content with whitespace
UC_WS_NL = UC + r'\s'  # content with whitespace, newline

UC_NWS = f'[{UC_NWS}]'
UC = f'[{UC}]'
UC_WS_NL = f'[{UC_WS_NL}]'

TEXT = fr"""
    (?P<text>
    {UC_NWS}        # ensure that text does not start with whitespace
    {UC_WS_NL}+?
    {UC_NWS}+?      # ensure that text does not end with whitespace
    )
"""

WHITESPACES = r'[ ]{1,5}'
WHITESPACES_OPT = r'[ ]{0,3}'
DOTTED = r'([ \.…]+)'
# TODO: ENSURE TO NOT CUTTING CONTENT WHICH ENDS: "BASS.10 => BASS PAGE: 10"
PAGE = r"""
    \b
    (?P<raw_page>
        ((S|P)\.[ ]{0,3})?      # optional S. or P.
        (?P<page>
            (
                \d{1,3}|                # arabic
                [IiVvXx]{1,6}           # roman
            )
        )
    )
    \b
"""

FLAGS = re.VERBOSE | re.MULTILINE | re.UNICODE | re.IGNORECASE

EXTENDED_PATTERN = re.compile(
    ('^'
     f'{LEVEL_DOTTED_OPTIONAL}'
     f'{WHITESPACES}'
     f'{TEXT}'
     f'{DOTTED}'
     f'{PAGE}'
     '$'),
    FLAGS,
)

EXTENDED_PATTERN_LETTER = re.compile(
    ('^'
     f'{LEVEL_LETTER}'
     f'{WHITESPACES}'
     f'{TEXT}'
     f'{DOTTED}'
     f'{PAGE}'
     '$'),
    FLAGS,
)

NO_DOTS = re.compile(
    ('^'
     f'{LEVEL_DOTTED_OPTIONAL}'
     f'{WHITESPACES}'
     f'{TEXT}'
     f'{WHITESPACES}'
     f'{PAGE}'
     '$'),
    FLAGS,
)

NO_LEVEL = re.compile(
    ('^'
     f'{TEXT}'
     f'{WHITESPACES_OPT}'
     f'{DOTTED}'
     f'{WHITESPACES_OPT}'
     f'{PAGE}'
     '$'),
    FLAGS,
)


def dictpattern() -> str:
    special = {'A'}
    headlines = special | elements.HEADLINES
    escaped = [re.escape(item) for item in headlines]
    result = '|'.join(escaped)
    return result


DICTIONARY = utila.compiles(
    '^'
    f'(?P<text>({dictpattern()}))'
    r'([ \.]{0,128})'
    f'{PAGE}',)


def extract_match(match: re.Match) -> reftable.toc.TocLine:
    assert isinstance(match, re.Match), type(match)
    level, title, page, raw_location = None, match['text'], None, None
    with contextlib.suppress(IndexError):
        page = match['page']
    with contextlib.suppress(IndexError):
        level = match['level']
    with contextlib.suppress(IndexError):
        level = level or match['backuplevel']
    with contextlib.suppress(IndexError):
        raw_location = match['raw_page']
    # prepare title
    title = utila.normalize_text(
        title,
        merge_divis=False,
        normalize_newline=True,
        normalize_spaces=True,
    )
    # create result
    result = reftable.toc.TocLine(
        level=level,
        title=title,
        page=page,
        raw=utila.extract_match(match),
        raw_level=level,
        pdfpage=raw_location,
    )
    return result


LINESTART = re.compile(
    rf"""
(
    ^{LEVEL_DOTTED_OPTIONAL.replace('level', 'backuplevel')}|
    ^{LEVEL_LETTER}|
    ^({dictpattern()})
)
     {WHITESPACES}
     {TEXT}
""",
    flags=re.VERBOSE | re.MULTILINE | re.IGNORECASE,
)
LINEEND = utila.compiles(PAGE + r'(\n|$)')
