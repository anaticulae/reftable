# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""toc result extraction decider
=============================

The decision strategy is implemented as a `ExtractionStatistic`-comparer
implemented in `__lt__` method.
"""

import dataclasses

import utila

import reftable.toc.strategy as gts


@dataclasses.dataclass(unsafe_hash=True)
class ExtractionStatistic:
    validitem_count: int
    group_count: int
    oneline_factor: float
    invalid_count: int = 0
    parsed_level: int = 0
    raw_length: int = 0
    strategy: str = None

    def __lt__(self, item):
        return better_than(self, item)


def better_than(
    current: ExtractionStatistic,
    other: ExtractionStatistic,
) -> bool:
    """"\
    1. Compare parsed levels
    2. Compare valid item count
    3. Compare online factor
    4. Compare raw length
    """
    # TODO: IMRPOVE THIS SIMPLE STRATEGY
    if current.invalid_count == other.invalid_count:
        if current.validitem_count == other.validitem_count:
            if current.parsed_level == other.parsed_level:
                if current.oneline_factor == other.oneline_factor:
                    return current.raw_length >= other.raw_length
                return current.oneline_factor < other.oneline_factor
            return current.parsed_level > other.parsed_level
        return current.validitem_count > other.validitem_count
    return current.invalid_count < other.invalid_count
    # # TODO: IMRPOVE THIS SIMPLE STRATEGY???
    # if current.parsed_level != other.parsed_level:
    #     return current.parsed_level >= other.parsed_level
    # if current.validitem_count != other.validitem_count:
    #     return current.validitem_count >= other.validitem_count
    # if current.oneline_factor != other.oneline_factor:
    #     return current.oneline_factor < other.oneline_factor
    # return current.raw_length >= other.raw_length


def decide(items: gts.ExtractionResults) -> gts.ExtractionResult:
    if not items:
        return None
    for item in items:
        utila.debug(item)
    analyzed = [analyze_result(item) for item in items]
    # debug result
    for item in analyzed:
        utila.debug(item)
    selector = dict(zip(analyzed, items))
    order = sorted(analyzed)
    first_item = order[0]
    selected = selector[first_item]
    return selected


def analyze_result(result: gts.ExtractionResult) -> ExtractionStatistic:
    # TODO: REMOVE FLATTEN
    # TODO: REMOVE valid_content = reftable.toc.strategy.group(valid_content)
    flat = utila.flat(result)
    oneliner = len([item for item in result if len(item) == 1])
    parsed_level = [item.level for item in flat if item.level is not None]
    oneline_factor = 0.0
    if len(result) >= 1:
        oneline_factor = utila.roundme(oneliner / len(result))  # pylint:disable=R0204
    result = ExtractionStatistic(
        validitem_count=len(flat),
        invalid_count=len(result.invalid),
        group_count=len(result),
        oneline_factor=oneline_factor,
        parsed_level=len(parsed_level),
        strategy=result.strategy,
        raw_length=sum(len(item.raw) for item in flat),
    )
    return result
