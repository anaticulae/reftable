# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elements
import utila

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
    oneline = utila.select_pages(oneline, pages=selected)
    if not headline_start(oneline[0]):
        utila.error(f'no valid figure headline start: {selected}')
        return []
    oneline = [
        reftable.toc.strategy.remove_headline(
            page,
            headlines=elements.FIGURETABLE,
        ) for page in oneline
    ]
    loaded = reftable.toc.strategy.ExtractionData(content=oneline)
    extracted = reftable.toc.run.extract(loaded)

    flat = utila.flatten(extracted.content)

    flat = remove_figure_sequence(flat)
    return flat


def headline_start(ptn) -> bool:
    """Verify that the first ptn starts with a valid figure table headline."""
    for line in ptn[0:8]:
        parsed = elements.headline.parser.parse_headline(line.text)
        if not parsed:
            continue
        if utila.verysimilar(parsed[0], expected=elements.FIGURETABLE):
            return True
    return False


FIGURE_REMOVE = utila.compiles(r"""
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
