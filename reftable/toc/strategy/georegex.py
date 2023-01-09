# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""table of content - geometry regex strategy
==========================================

Use the geometry of the page to extract the table of content.

Strategy:

* split area by `GROUP_GAP_MIN`
    * run regex for every item in group
    * group items which not pass the parser
    * run parser on grouped items
* merge extracted groups to get table of content over pages
* validate extracted toc

"""

import configo
import texmex
import utila

import reftable.toc
import reftable.toc.basic.group
import reftable.toc.strategy

GROUP_GAP_MIN = configo.HV_FLOAT_PLUS(default=30.0)


class GeometryRegexTocExtractor(reftable.toc.strategy.ExtractorStrategy):

    def result(self) -> reftable.toc.strategy.ExtractionResult:
        extracted = [analyse_page(item) for item in self.loaded]
        flat = utila.flat(utila.flat(extracted))
        result = self.finalize_result(flat)
        return result


def analyse_page(content: texmex.PTN) -> reftable.toc.TocLines:
    assert isinstance(content, texmex.NavigatorMixin), type(content)
    content = reftable.toc.strategy.remove_headline(content)
    grouped = group_areas(content)
    result = [
        reftable.toc.basic.group.parse_group(items, page=content.page)
        for items in grouped
    ]
    # remove not parsed
    result = utila.notempty(result)
    return result


def group_areas(content: texmex.PTN) -> list:
    if not content:
        return []
    linedistances = texmex.linedistances(content, noneatend=False)
    result = []
    grouped = []
    for item, distance in zip(content, linedistances):
        grouped.append(item)
        if distance > GROUP_GAP_MIN:
            result.append(grouped)
            grouped = []
    # add last one, cause last one has no linedistance
    grouped.append(content[-1])
    if grouped:
        result.append(grouped)
    return result
