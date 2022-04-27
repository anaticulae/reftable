# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila

import reftable
import tests


@pytest.mark.parametrize('source, expected, pages', [
    pytest.param(power.BACHELOR076_PDF, 42, 2, id='bachelor76'),
])
def test_abbreviation_validate(source, expected, pages, monkeypatch, testdir):
    source = power.link(source)
    pages = (pages,) if isinstance(pages, int) else pages
    pages: str = utila.from_tuple(pages, separator=',') if pages else ':'
    cmd = f'-i {source} --abbrev --pages={pages}'
    tests.run(cmd, monkeypatch=monkeypatch)

    toc = reftable.path.abbreviation(testdir.tmpdir)
    toc = serializeraw.load_abbreviation_table(toc)

    assert len(toc) == expected
