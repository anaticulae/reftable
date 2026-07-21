# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of figures extractor
==========================
"""

import configos
import elementae
import iamraw
import serializeraw
import utilo

import reftable.pageselector
import reftable.toc.create
import reftable.toc.run

# minimal percentage of tabletable lines per page
TOFS_PER_PAGE_MIN = configos.HV_PERCENT_PLUS(default=20, limit=100)


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
    navigators = serializeraw.ptcn_fromfile(
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
    navigators = utilo.select_pages(navigators, pages=selected)
    if not headline_start(navigators[0]):
        utilo.error(f'no valid table headline start: {selected}')
        return EMPTY
    # run
    extracted = reftable.toc.run.extract(navigators)
    # prepare
    flat = utilo.flat(extracted.content)
    leveled = reftable.toc.create.groupby_level(flat)
    # dump
    dumped = serializeraw.dump_toc(leveled)
    return dumped


EMPTY = serializeraw.dump_toc(iamraw.Toc())
NO_TABLES = utilo.unique(elementae.ABBREVIATION + elementae.TOC +
                         elementae.FIGURETABLE + elementae.SYMBOLTABLE)


def headline_start(ptn) -> bool:
    """Verify that the first ptn starts with a valid figure table headline."""
    # TODO: INTEGRATE INTO SELECT_CONTENTPAGES
    for line in ptn[0:8]:
        parsed = elementae.headline.parser.parse_headline(line.text)
        if not parsed:
            continue
        if utilo.verysimilar(parsed[0], expected=elementae.TABLETABLE):
            return True
    return False
