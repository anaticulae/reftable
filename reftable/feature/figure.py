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

import serializeraw

import reftable.figure.strategy


def work(
    text: str,
    textpositions: str,
    oneline_text: str,
    oneline_textpositions: str,
    headerfooter: str,
    sizeandborder: str,
    pages: tuple = None,
) -> str:
    """Extract table of figures out of `document`.

    Args:
        text(str): path to load document
        textpositions(str): path to load document textpositions
        oneline_text(str): oneline document
        oneline_textpositions(str): oneline document positions
        headerfooter(str): path with header and footer to determine
                           content border.
        sizeandborder(str): path with page sizes and content border
        pages(tuple): tuple of selected pages
    Returns:
        dump of extracted table of content
    """
    result = reftable.figure.strategy.run(
        text=text,
        textpositions=textpositions,
        oneline_text=oneline_text,
        oneline_textpositions=oneline_textpositions,
        headerfooter=headerfooter,
        sizeandborder=sizeandborder,
        pages=pages,
    )
    dumped = serializeraw.dump_toc(result)
    return dumped
