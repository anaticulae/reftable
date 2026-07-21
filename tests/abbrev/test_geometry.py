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

import reftable.abbrev.geometry


def bachelor37():
    content = serializeraw.ptn_frompath(
        hoverpower.link(hoverpower.BACHELOR037_PDF),
        pages=2,
    )
    content = reftable.abbrev.AbbreviationData(normal=content)
    return content


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(hoverpower.BACHELOR037_PDF, 1, 26, id='bachelor37_abbrev'),
    pytest.param(hoverpower.BACHELOR037_PDF, 2, 10, id='bachelor37_figure'),
    pytest.param(hoverpower.HOME050_PDF, 6, 0, id='homework50'),
    pytest.param(hoverpower.MASTER116_PDF, 96, 8, id='master116'),
])
@utilotest.longrun
def test_abbreviation_parse_strategy_geometry(source, pages, expected):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    content = serializeraw.ptn_frompath(
        source,
        pages=pages,
    )
    content = reftable.abbrev.AbbreviationData(normal=content)
    strategy = reftable.abbrev.geometry.GeometryAbbreviationParser(content)
    parsed = strategy.result()
    assert len(parsed) == expected, len(parsed)
