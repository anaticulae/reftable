# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import texmex
import utilo

import reftable.toc.decider
import reftable.toc.strategy
import reftable.toc.strategy.balance
import reftable.toc.strategy.geometry
import reftable.toc.strategy.georegex
import reftable.toc.strategy.pagetop
import reftable.toc.strategy.regex


def extract(
    data: texmex.NavigatorMixins,
    active: list = None,
    min_detection_count: int = 1,
) -> reftable.toc.strategy.ExtractionResult:
    """Run various strategies to extract ``toc-lines`` out of given ``data``.

    Args:
        data: loaded data
        active: List of executed stratgies. Use ``None`` to run all
                strategies.
        min_detection_count: if count of valid results is lower, return
                             empty result
    Returns:
        List of ``ExtractionResult`` with extracted data.
    """
    strategies = [
        reftable.toc.strategy.geometry.GeometryTocExtractor,
        reftable.toc.strategy.georegex.GeometryRegexTocExtractor,
        reftable.toc.strategy.regex.RegexTocExtractor,
        reftable.toc.strategy.balance.BalanceTocExtractor,
        reftable.toc.strategy.pagetop.PageTop,
    ]
    results = [
        strategy(data).result()
        for strategy in strategies
        # decide if strategy is active
        if active is None or strategy in active
    ]
    decision = reftable.toc.decider.decide(results)
    if len(utilo.flat(decision.content)) < min_detection_count:
        decision = reftable.toc.strategy.ExtractionResult()
    return decision
