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
import serializeraw
import utilotest

import reftable.abbrev.simple


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(hoverpower.HOME050_PDF, 6, 18, id='homework50'),
    pytest.param(hoverpower.MASTER116_PDF, 96, 8, id='master116'),
    pytest.param(
        hoverpower.BACHELOR037_PDF,
        1,
        26,
        id='bachelor37',
        marks=pytest.mark.xfail(reason='require more complex strategy'),
    ),
])
@utilotest.longrun
def test_abbreviation_parse_simple(source, pages, expected):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
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
