# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of content extractor
==========================

Outdated approaches
-------------------

- collect title and check if sequence exists again in the document

"""

import configos
import elementae
import elementae.headline.lookup
import serializeraw
import utilo

import reftable.feature
import reftable.pageselector
import reftable.toc
import reftable.toc.create
import reftable.toc.run
import reftable.toc.strategy

# minimal percentage of toc lines per page
TOCS_PER_PAGE_MIN = configos.HV_PERCENT_PLUS(default=30, limit=100)

# limit possible toc to the first 15 pages
POSSIBLE_PAGES = utilo.make_tuple(15)

TOC_COUNT_MIN = configos.HV_INT_PLUS(default=4)


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
    navigators = serializeraw.ptcn_fromfile(
        text,
        textpositions,
        sizeandborder=sizeandborder,
        headerfooter=headerfooter,
        pages=pages,
    )
    extracted = run(navigators)
    dumped = dump(extracted)
    return dumped


def run(navigators):
    selected = reftable.pageselector.select_contentpages(
        textnavigators=navigators,
        wrong_table=NO_TOC,
        skip_higherqual_level_three=False,
        valid_lines_perpage_min=TOCS_PER_PAGE_MIN,
    )
    navigators = utilo.select_pages(
        navigators,
        pages=selected,
    )
    extracted = reftable.toc.run.extract(
        navigators,
        min_detection_count=TOC_COUNT_MIN,
    )
    return extracted


def dump(extracted):
    flat = utilo.flat(extracted.content)
    leveled = reftable.toc.create.groupby_level(flat)
    leveled.__strategy__ = extracted.strategy
    dumped = serializeraw.dump_toc(leveled)
    return dumped


# NO_TOC = elementae.headline.lookup.HEADLINES - elementae.headline.lookup.TOC
NO_TOC = [
    item for item in elementae.headline.lookup.HEADLINES
    if item not in elementae.headline.lookup.TOC
]
