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

import reftable.abbrev.geometry


def bachelor37():
    content = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.BACHELOR037_PDF),
        pages=2,
    )
    content = reftable.abbrev.AbbreviationData(normal=content)
    return content


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(power.BACHELOR037_PDF, 1, 26, id='bachelor37_abbrev'),
    pytest.param(power.BACHELOR037_PDF, 2, 10, id='bachelor37_figure'),
    pytest.param(power.HOME050_PDF, 6, 0, id='homework50'),
    pytest.param(power.MASTER116_PDF, 96, 8, id='master116'),
])
@utilatest.longrun
def test_abbreviation_parse_strategy_geometry(source, pages, expected):
    utilatest.fixture_requires(source)
    source = power.link(source)
    content = serializeraw.create_pagetextnavigators_frompath(
        source,
        pages=pages,
    )
    content = reftable.abbrev.AbbreviationData(normal=content)
    strategy = reftable.abbrev.geometry.GeometryAbbreviationParser(content)
    parsed = strategy.result()
    assert len(parsed) == expected, len(parsed)
