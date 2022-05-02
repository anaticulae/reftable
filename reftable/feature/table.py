# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of figures extractor
==========================
"""

import configo
import elements
import iamraw
import serializeraw
import utila

import reftable.pageselector
import reftable.toc.create
import reftable.toc.run
import reftable.toc.strategy

# minimal percentage of tabletable lines per page
TOFS_PER_PAGE_MIN = configo.HV_PERCENT_PLUS(default=20, limit=100)


def work(
    text: str,
    textpositions: str,
    headerfooter: str,
    sizeandborder: str,
    pages: tuple = None,
) -> str:
    """Extract table of figures out of `document`.

    Args:
        text(str): path to load document
        textpositions(str): path to load document textpositions
        headerfooter(str): path with header and footer to determine
                           content border.
        sizeandborder(str): path with page sizes and content border
        pages(tuple): tuple of selected pages
    Returns:
        dump of extracted table of content
    """
    navigators = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textpositions,
        sizeandborder=sizeandborder,
        headerfooter=headerfooter,
        pages=pages,
    )
    selected = reftable.pageselector.select_contentpages(
        navigators,
        wrong_table=NO_TABLES,
        valid_lines_perpage_min=TOFS_PER_PAGE_MIN,
    )
    if not selected:
        return EMPTY
    # select toc pages only
    navigators = utila.select_pages(navigators, pages=selected)
    if not headline_start(navigators[0]):
        utila.error(f'no valid table headline start: {selected}')
        return EMPTY
    loaded = reftable.toc.strategy.ExtractionData(content=navigators)
    # run
    extracted = reftable.toc.run.extract(loaded)
    # prepare
    flat = utila.flatten(extracted.content)
    leveled = reftable.toc.create.groupby_level(flat)
    # dump
    dumped = serializeraw.dump_toc(leveled)
    return dumped


EMPTY = serializeraw.dump_toc(iamraw.Toc())
NO_TABLES = (elements.ABBREVIATION | elements.TOC | elements.FIGURETABLE |
             elements.SYMBOLTABLE)


def headline_start(ptn) -> bool:
    """Verify that the first ptn starts with a valid figure table headline."""
    # TODO: INTEGRATE INTO SELECT_CONTENTPAGES
    for line in ptn[0:8]:
        parsed = elements.headline.parser.parse_headline(line.text)
        if not parsed:
            continue
        if utila.verysimilar(parsed[0], expected=elements.TABLETABLE):
            return True
    return False
