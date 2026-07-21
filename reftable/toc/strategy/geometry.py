# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""table of content - geometry strategy
====================================
"""

import functools

import configos
import texmex
import utilo

import reftable.toc.basic.group
import reftable.toc.strategy

HEADLINE_LEVEL_MAX = configos.HV_INT_PLUS(default=3)


class GeometryTocExtractor(reftable.toc.strategy.ExtractorStrategy):

    def result(self) -> reftable.toc.strategy.ExtractionResult:
        extracted = []
        for page in self.loaded:
            analyzed = analyse_page(page, level_feeds=self.textfeed)
            analyzed = remove_pagenumber_headline(analyzed)
            extracted.extend(analyzed)
        grouped = group_areas(extracted)
        content = [
            reftable.toc.basic.group.parse_group(group, page)
            for page, group in grouped
        ]
        content = utilo.notempty(content)
        content = utilo.flat(content)
        result = self.finalize_result(content)
        return result

    @functools.cached_property
    def textfeed(self):
        feeds = texmex.document_textfeed(
            self.loaded,
            count=HEADLINE_LEVEL_MAX.value,
        )
        feed = sorted(feeds)
        return feed


def analyse_page(
    navigator: texmex.PTCNs,
    level_feeds: list,
) -> list:
    contentborder = navigator.content
    # TODO: SHRINK TO FIRST OCCURRENCE? OR IS THIS NOT NECESSARY
    navigator: 'PTN' = reftable.toc.strategy.remove_headline(navigator)
    textbounds = texmex.textbounds(navigator, contentborder)
    result = []
    for item in textbounds:
        # document_text feed is computed from left page border to text.
        # text feed is computed from expected content start till text start
        # convert local to global text feed
        xdist = contentborder.left + item.bounds.leftdist
        current_level = level(xdist, level_feeds)
        result.append((navigator.page, (current_level, item)))
    return result


def group_areas(items):
    result = []
    current = []
    lastpage = -1
    for page, (level_, item) in items:
        if current:
            if page >= (lastpage + 1):
                # one page space between toc groups, the toc can not be
                # connected.
                result.append((lastpage, current))
                current = []
            elif level_ == 0:  # pylint:disable=C2001
                # new group
                result.append((page, current))
                current = []
            # continue
        current.append(item)
        lastpage = page
    if current:
        result.append((lastpage, current))
    return result


def level(xdist, levels):
    for index, item in enumerate(levels):
        if xdist <= item:
            return index
    return None


PAGENUMBER_HEADLINE = utilo.splitlines("""
Page
Pages
Seite
""")

# max distance from content border to text start
RIGHTDIST_MAX = configos.HV_INT_PLUS(default=80)


def remove_pagenumber_headline(content):
    """Remove Page over number of pages.

    See:

    TABLE OF CONTENTS
                                                                       Page
    LIST OF FIGURES .....................................................vi
    LIST OF TABLES......................................................vii
    """
    result = []
    for item in content[0:5]:
        # (4, (None, TextBoundsInfo(text='Page\n', bounds=TextBounds(...))))
        bounding = item[1][1].bounds
        # right text orientation
        if bounding.rightdist < RIGHTDIST_MAX:
            text = item[1][1].text
            if utilo.verysimilar(
                    current=text,
                    expected=PAGENUMBER_HEADLINE,
            ):
                continue
        result.append(item)
    result.extend(content[5:])
    return result
