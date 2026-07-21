# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elementae
import utilo

import reftable.figure
import reftable.pageselector
import reftable.toc.run
import reftable.toc.strategy


def run(oneline) -> list:
    selected = reftable.pageselector.select_contentpages(
        oneline,
        wrong_table=reftable.figure.NO_FIGURES,
        valid_lines_perpage_min=reftable.figure.TOFS_PER_PAGE_MIN,
    )
    if not selected:
        return []
    # select figure pages only
    oneline = utilo.select_pages(oneline, pages=selected)
    if not headline_start(oneline[0]):
        utilo.error(f'no valid figure headline start: {selected}')
        return []
    oneline = [
        reftable.toc.strategy.remove_headline(
            page,
            headlines=elementae.FIGURETABLE,
        ) for page in oneline
    ]
    extracted = reftable.toc.run.extract(oneline)
    flat = utilo.flat(extracted.content)
    flat = remove_figure_sequence(flat)
    return flat


def headline_start(ptn) -> bool:
    """Verify that the first ptn starts with a valid figure table headline."""
    for line in ptn[0:8]:
        parsed = elementae.headline.parser.parse_headline(line.text)
        if not parsed:
            continue
        if utilo.verysimilar(parsed[0], expected=elementae.FIGURETABLE):
            return True
    return False


FIGURE_REMOVE = utilo.compiles(r"""
    ^
    (
        ABBILDUNG|
        ABB\.?|
        FIGURE|
        FIG.?
    )
    [ ]{0,2}
    \d{1,3}
    \:
    [ ]{0,2}
""")


def remove_figure_sequence(items) -> list:
    """Remove starting sequence which is a result of using toc-table
    parser."""
    for item in items:
        item.title = FIGURE_REMOVE.sub('', item.title)
    return items
