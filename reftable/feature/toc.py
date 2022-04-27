# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of content extractor
==========================

Outdated approaches
-------------------

- collect title and check if sequence exists again in the document

"""

import configo
import elements
import serializeraw
import utila

import reftable.feature
import reftable.toc
import reftable.toc.run
import reftable.toc.strategy
import reftable.toc.create

# minimal percentage of toc lines per page
TOCS_PER_PAGE_MIN = configo.HV_PERCENT_PLUS(default=30, limit=100)

# limit possible toc to the first 15 pages
POSSIBLE_PAGES = utila.make_tuple(15)

TOC_COUNT_MIN = configo.HV_INT_PLUS(default=4)


def work(
    text: str,
    textpositions: str,
    headerfooter: str,
    sizeandborder: str,
    pages: tuple = None,
) -> str:
    """Extract table of content out of `document`.

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
    pages = POSSIBLE_PAGES if pages is None else pages
    navigators = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textpositions,
        sizeandborderpath=sizeandborder,
        headerfooterpath=headerfooter,
        pages=pages,
    )
    selected = reftable.pageselector.select_contentpages(
        textnavigators=navigators,
        wrong_table=NO_TOC,
        skip_higherqual_level_three=False,
        valid_lines_perpage_min=TOCS_PER_PAGE_MIN,
    )
    navigators = utila.select_pages(navigators, pages=selected)
    loaded = reftable.toc.strategy.ExtractionData(content=navigators)
    extracted = reftable.toc.run.extract(
        loaded,
        min_detection_count=TOC_COUNT_MIN,
    )

    flat = utila.flatten(extracted.content)
    leveled = reftable.toc.create.groupby_level(flat)
    leveled.__strategy__ = extracted.strategy
    dumped = serializeraw.dump_toc(leveled)
    return dumped


NO_TOC = elements.headline.lookup.HEADLINES - elements.headline.lookup.TOC
