# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import texmex
import utila

import reftable.toc.basic.group
import reftable.toc.basic.lineregex


class BalanceTocExtractor(reftable.toc.strategy.ExtractorStrategy):

    def result(self) -> reftable.toc.strategy.ExtractionResult:
        extracted = [analyse_page(item) for item in self.loaded.content]
        flat = utila.flatten(extracted)
        result = self.finalize_result(flat)
        return result


def analyse_page(navigator: texmex.PageTextContentNavigators) -> list:
    navigator: 'PTN' = reftable.toc.strategy.remove_headline(navigator)
    raw: str = navigator.debug
    raw = utila.normalize_text(
        raw,
        merge_divis=False,
        normalize_newline=False,
        normalize_spaces=True,
    )
    lines = borders_best(raw)
    result = []
    for item in lines:
        if not item.strip():
            continue
        item = utila.normalize_whitespaces(item)
        parsed = reftable.toc.basic.lineregex.parse(item)
        if not parsed:
            # backup strategy with page number
            parsed = reftable.toc.basic.lineregex.parse_linestart(item)
        if not parsed:
            short = utila.shrink(item, maxlength=70)
            utila.debug(f'could not backup parse: {short}')
            continue
        result.append(parsed)
    reftable.toc.basic.group.set_pagelocation(
        result,
        page=navigator.page,
    )
    return result


def borders_best(raw: str) -> list:
    starts, ends = [], []
    for matched in reftable.toc.basic.lineregex.LINESTART.finditer(raw):
        starts.append(matched.start())
    starts = [0] + starts if 0 not in starts else starts
    for matched in reftable.toc.basic.lineregex.LINEEND.finditer(raw):
        ends.append(matched.end())
    zipped = zip_best(starts, ends)
    solved = solve_none(zipped)
    lines = [raw[item[0]:item[1]] for item in solved]
    return lines


def zip_best(starts, ends) -> list:
    """\
    >>> zip_best([0, 104, 119, 220, 392, 491, 586, 716, 813, 913], [102, 218, 389, 488, 583, 713, 910, 1008])
    [(0, 102), (104, None), (119, 218), (220, 389), (392, 488), (491, 583), (586, 713), (716, None), (813, 910), (913, 1008)]
    >>> zip_best([0, 80, 230, 377, 532, 680, 834, 979, 1397, 1526, 1675, 1985], [229, 376, 531, 679, 833, 978, 1112, 1256, 1396, 1525, 1674, 1829, 1984, 2128, 2129])
    [(0, None), (80, 229), (230, 376), (377, 531), (532, 679), (680, 833), (834, 978), (979, 1112), (None, 1256), (None, 1396), (1397, 1525), (1526, 1674), (1675, 1829), (None, 1984), (1985, 2128), (None, 2129)]

    1. Connect every end with the nearest starts item before which is not before nearest end item
    2. Do this for every ends
    3. After all ends are processed, insert every start items which are left
    4. Sort result by first index
    """
    starts, ends = sorted(starts), sorted(ends)
    pairs = []
    while ends:
        current = ends[-1]
        ends = ends[0:-1]
        lower = ends[-1] if ends else -1
        matched = [item for item in starts if lower <= item < current]
        if matched:
            pairs.append((matched[-1], current))
            starts.remove(matched[-1])
        else:
            pairs.append((None, current))
    for item in starts:
        pairs.append((item, None))
    pairs = sorted(pairs, key=lambda x: x[0] if x[0] is not None else x[1])
    return pairs


def solve_none(items) -> list:
    """\
    >>> solve_none([(0, None), (80, 230), (230, 376), (377, 532), (532, 680), (680, 834),
    ... (834, 979), (979, 1112), (None, 1256), (None, 1397), (1397, 1526), (1526, 1674),
    ... (1674, 1829), (None, 1985), (1985, 2129), (None, 2129)])
    [(0, 80), (80, 230), (230, 376), (377, 532), (532, 680),...(1829, 1985), (1985, 2129), (2129, 2129)]
    """
    if not items:
        return []
    result = [items[0]]
    for item in items[1:]:
        if result[-1][-1] is None:
            result[-1] = (result[-1][0], item[0])
        if item[0] is None:
            item = result[-1][1], item[1]
        result.append(item)
    return result
