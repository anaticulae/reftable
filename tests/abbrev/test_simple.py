# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest

import reftable.abbrev.simple


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.HOME050_PDF, 6, 18, id='homework50'),
    pytest.param(power.MASTER116_PDF, 96, 8, id='master116'),
    pytest.param(
        power.BACHELOR037_PDF,
        1,
        26,
        id='bachelor37',
        marks=pytest.mark.xfail(reason='require more complex strategy'),
    ),
])
@utilatest.longrun
def test_abbreviation_parse_simple(source, pages, expected):
    utilatest.fixture_requires(source)
    source = power.link(source)
    content = serializeraw.ptn_frompath(
        source,
        prefix='oneline',
        pages=pages,
    )
    content = reftable.abbrev.AbbreviationData(oneline=content)
    strategy = reftable.abbrev.simple.SimpleAbbreviationParser(content)
    parsed = strategy.result()
    assert parsed, parsed
    assert len(parsed) == expected, str(parsed)
