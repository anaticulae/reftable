# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""PageTop
=======

Example
-------

.. code-block :: none

    1. Vier in Serie: Die Piraten als neuer Akteur im                  S. 3
       Parteienwettbewerb

    2. Theorie und Operationalisierung                                 S. 5
    2.1. Ein modifiziertes Modell zur Erklärung von Wahlverhalten      S. 5
    2.1.1. Der soziologische Ansatz                                    S. 6
    2.1.2. Der sozialpsychologische Ansatz unter Berücksichtigung      S. 9
           der Modifikation von Brettschneider 2001
    2.2. Operationalisierung                                           S. 13
"""

import re

import texmex
import utila

import reftable.toc.basic.group
import reftable.toc.basic.lineregex
import reftable.toc.strategy
import reftable.toc.strategy.regex


class PageTop(reftable.toc.strategy.ExtractorStrategy):

    def result(self) -> reftable.toc.strategy.ExtractionResult:
        extracted = [analyse_page(item) for item in self.loaded]
        flat = utila.flat(extracted)
        result = self.finalize_result(flat)
        return result


def analyse_page(navigator: texmex.PTCNs) -> list:
    navigator: 'PTN' = reftable.toc.strategy.remove_headline(navigator)
    raw = navigator.debug
    raw = re.sub(r'\n(S\. \d{1,3})', r' \1', raw)
    lines = raw.splitlines()
    parsed = reftable.toc.strategy.regex.parse_page(navigator)
    if not parsed:
        return []
    matched = [[
        index
        for index, line in enumerate(lines)
        if utila.verysimilar(expected=item.raw, current=line)
    ]
               for item in parsed]
    single_match_only = set(len(item) for item in matched) == {1}
    if not single_match_only:
        # a toc line can always occurs only once, may this is not the
        # right strategy.
        return []
    result = []
    for index, (current, after) in enumerate(zip(matched[0:-1], matched[1:])):
        todo = current[0] + 1 != after[0]
        if not todo:
            result.append(parsed[index])
            continue
        item = parsed[index]
        for append in utila.rlist(start=current[0] + 1, end=after[0]):
            item.title += ' ' + lines[append]
            item.raw += ' ' + lines[append]
        result.append(item)
    if len(parsed) > 1:
        result.append(parsed[-1])
    # TODO: INVESTIGATE BACHELOR105 HEADLINES AT THE END OF THE PAGE/TOC
    return result
