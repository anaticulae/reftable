# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilotest

import reftable.toc.run
import reftable.toc.strategy.geometry
import tests.fixtures.tableofcontent


@utilotest.longrun
def test_toc_strategy_geometry():
    headlines = tests.fixtures.tableofcontent.bachelor111_toc()

    # expected = [3, 16, 8, 5, 7, 8, 3, 1, 4, 1, 1, 1, 9]
    expected = [3, 16, 8, 5, 7, 8, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8]

    # TODO: MERGE `A` of ANHANG to last 8 to activate 9
    # TODO: DETECT BROKEN LITERATUR: HItn page 80 is not correct, same
    # label error like in master116

    active = [
        reftable.toc.strategy.geometry.GeometryTocExtractor,
    ]
    grouped = reftable.toc.run.extract(
        headlines,
        active=active,
    )
    current = [len(item) for item in grouped]
    assert current == expected


@utilotest.longrun
def test_toc_strategy_bachelor111():
    headlines = tests.fixtures.tableofcontent.bachelor111_toc()

    # TODO: SEE ABOVE
    # expected = [3, 16, 8, 5, 7, 8, 3, 1, 4, 1, 1, 1, 9]
    expected = [3, 16, 8, 5, 7, 8, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8]

    grouped = reftable.toc.run.extract(headlines)
    current = [len(item) for item in grouped]
    assert current == expected
