# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import geostrat
import utilo

import reftable.figure
import reftable.pageselector
import reftable.toc


def run(ptcns) -> list:
    """\
    Abb. 1      SAM Skala in der 9-Punkte-Likert-Form
    Abb. 2      Mittelwerte der N ormierungen v on Lang et a l. ( 2005) und
                Libkuman et al. (2007)
    """
    pages = reftable.pageselector.select_contentpages(
        ptcns,
        strategy=parse,
        wrong_table=reftable.figure.NO_FIGURES,
        valid_lines_perpage_min=reftable.figure.TOFS_PER_PAGE_MIN,
    )
    if not pages:
        return []
    ptcns = utilo.select_pages(ptcns, pages)
    extracted = [parse(item) for item in ptcns]
    result = utilo.flat(extracted)
    return result


def parse(ptcn) -> reftable.toc.TocLines:
    parsed = geostrat.dc_parse_page(ptcn)
    if not parsed:
        return []
    result = []
    for level, title in parsed:
        if not check_level(level):
            utilo.debug(f'invalid figure level: {level}')
            continue
        item = reftable.toc.TocLine(
            level=level,
            title=title,
            pdfpage=ptcn.page,
        )
        result.append(item)
    return result


LEVEL_START = utilo.compiles(r"""
    ^
    (
        ABBILDUNG|
        ABB\.?|
        FIGURE|
        FIG\.?
    )
""")


def check_level(item: str):
    """\
    >>> check_level('Abb. 1      SAM Skala')
    True
    """
    item = item.strip()
    if LEVEL_START.match(item):
        return True
    return False
