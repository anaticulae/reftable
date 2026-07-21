# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import reftable
import tests


@pytest.mark.parametrize('source, expected, pages', [
    pytest.param(hoverpower.BACHELOR076_PDF, 42, 2, id='bachelor76'),
])
def test_abbreviation_validate(source, expected, pages, mp, td):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    pages = (pages,) if isinstance(pages, int) else pages
    pages: str = utilo.from_tuple(pages, separator=',') if pages else ':'
    cmd = f'-i {source} --abbrev --pages={pages}'
    tests.run(cmd, mp=mp)

    toc = reftable.path.abbreviation(td.tmpdir)
    toc = serializeraw.load_abbreviation_table(toc)
    assert len(toc) == expected
