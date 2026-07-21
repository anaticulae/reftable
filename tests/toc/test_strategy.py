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
import tests.fixtures.tableofcontent


@utilotest.longrun
def test_toc_strategy_master72():
    """Headline 3.1. is writen over content border, therefore we have to
    disable checking content border in PTCN
    creation. If we do not, the third position `11` detects only `10`
    headlines."""
    headlines = tests.fixtures.tableofcontent.master72_toc()
    expected = [3, 9, 11, 6, 1, 1, 1]
    grouped = reftable.toc.run.extract(headlines)
    assert len(grouped) == len(expected)
    # verify
    count = [len(item) for item in grouped]
    assert count == expected


@utilotest.longrun
def test_toc_strategy_technial24():
    headlines = tests.fixtures.tableofcontent.technical24_toc()
    expected = [1, 1, 2, 7, 5, 1, 16, 1]
    grouped = reftable.toc.run.extract(headlines)
    assert len(grouped) == len(expected)
