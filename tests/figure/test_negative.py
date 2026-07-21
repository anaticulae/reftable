# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import utilotest

import tests.table


@pytest.mark.parametrize('source, pages', [
    pytest.param(
        hoverpower.MASTER089_PDF,
        (85, 86, 87, 88),
        id='master89_page85_86_87_88',
    ),
    pytest.param(
        hoverpower.BACHELOR111_PDF,
        (0, 1, 2, 3, 4, 5, 6),
        id='bachelor111document_start',
    ),
])
@utilotest.nightly
def test_regression_non_valid_examples(source, pages, mp, td):
    source = hoverpower.link(source)
    extracted = tests.figure.extract_table(
        source,
        pages,
        mp,
        td,
    )
    assert not extracted
