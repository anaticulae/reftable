# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import reftable.toc.decider

EXAMPLE = [
    reftable.toc.decider.ExtractionStatistic(
        validitem_count=67,
        group_count=13,
        oneline_factor=0.31,
    ),
    reftable.toc.decider.ExtractionStatistic(
        validitem_count=67,
        group_count=17,
        oneline_factor=0.53,
    ),
    reftable.toc.decider.ExtractionStatistic(
        validitem_count=64,
        group_count=17,
        oneline_factor=0.53,
    ),
]


def test_toc_decider_sort_decisions():
    assert sorted(EXAMPLE) == EXAMPLE
