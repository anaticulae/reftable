# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation Parser: Geometry Strategy
======================================

This approach splits the page in two columns and detect a left shortcut
and a right description column. It is required that the distance between
left and right column is not ?too? tight.

Working Examples
----------------

* bachelor37: page 2

Not working
-----------

* homework50: columns are to tight together

Nearly working
--------------

* master116: improve layout parser
"""

import geostrat
import iamraw
import texmex
import utila

import reftable.abbrev


class GeometryAbbreviationParser(reftable.abbrev.AbbreviationExtractorStrategy):

    def result(self) -> iamraw.AbbreviationResult:
        ready = iamraw.AbbreviationResult()
        for page in self.loaded.normal:
            parsed = parse_page(page)
            if parsed is None:
                utila.info(f'could not parse page: {page.page}')
                continue
            for item in parsed:
                ready.append(item)
            ready.pdfpages.append(page.page)
        return ready


def parse_page(page: texmex.PTN) -> iamraw.Abbreviations:
    parsed = geostrat.dc_parse_page(page)
    if not parsed:
        return None
    result = []
    for short, description in parsed:
        short, description = short.strip(), description.strip()
        description = description.lstrip('-')
        result.append(
            iamraw.Abbreviation(
                short=short,
                description=description,
                position=iamraw.AbbreviationPosition(page=page.page),
            ))
    return result
