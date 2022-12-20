# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest

import reftable.abbrev
import reftable.abbrev.parser


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR037_PDF, 1, 26, id='bachelor37'),
    pytest.param(power.HOME050_PDF, 6, 18, id='homework50'),
    pytest.param(power.MASTER116_PDF, 96, 8, id='master116'),
    pytest.param(power.DISS205_PDF, 14, 17, id='diss205'),
])
@utilatest.longrun
def test_abbreviation_parser(source, pages, expected):
    utilatest.fixture_requires(source)
    source = power.link(source)
    normal = serializeraw.ptn_frompath(
        source,
        pages=pages,
    )
    oneline = serializeraw.ptn_frompath(
        source,
        prefix='oneline',
        pages=pages,
    )
    content = reftable.abbrev.AbbreviationData(
        normal=normal,
        oneline=oneline,
    )
    result = reftable.abbrev.parser.parse(content)
    assert result, result
    assert len(result) == expected, str(result)
