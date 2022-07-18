# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import elements
import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import reftable
import reftable.toc.run
import reftable.toc.strategy
import tests

ARCHIVE = utila.join(reftable.ROOT, 'tests/toc/expected', exist=True)
TEN = utila.make_tuple(10)


@pytest.mark.parametrize('source, pages', [
    utilatest.step(power.BACHELOR028_PDF, (1,)),
    utilatest.step(power.BACHELOR032A_PDF, (1,)),
    utilatest.step(power.BACHELOR032_PDF, (1,)),
    utilatest.step(power.BACHELOR039_PDF, (1,)),
    utilatest.step(power.BACHELOR041A_PDF, (1,)),
    utilatest.step(power.BACHELOR063_PDF, TEN),
    utilatest.step(power.BACHELOR076_PDF, TEN),
    utilatest.step(power.BACHELOR078_PDF, (1,)),
    utilatest.step(power.BACHELOR086_PDF, (1,)),
    utilatest.step(power.BACHELOR090_PDF, TEN),
    utilatest.step(power.BACHELOR101_PDF, (1, 2)),
    utilatest.step(power.BACHELOR105_PDF, (1, 2)),
    utilatest.step(power.BACHELOR111_PDF, (1, 2, 3, 4)),
    utilatest.step(power.BACHELOR128_PDF, (3, 4, 5)),
    utilatest.step(power.BACHELOR241_PDF, (4, 5, 6, 7)),
    utilatest.step(power.BOOK173_PDF, (9, 10, 11, 12)),
    utilatest.step(power.DISS157_PDF, (6, 7, 8)),
    utilatest.step(power.DISS172_PDF, (7, 8)),
    utilatest.step(power.DISS178_PDF, (3, 4)),
    utilatest.step(power.DISS180_PDF, (4, 5)),
    utilatest.step(power.DISS406_PDF, (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)),
    utilatest.step(power.DISS480_PDF, (2, 3)),
    utilatest.step(power.HC_DISS128, (6, 7)),
    utilatest.step(power.HC_DISS148, (6, 7)),
    utilatest.step(power.HC_DISS166, (6, 7)),
    utilatest.step(power.HC_DISS171, (8, 9, 10)),
    utilatest.step(power.HC_DISS193, (9, 10, 11, 12)),
    utilatest.step(power.HOME050_PDF, (3, 4)),
    utilatest.step(power.MASTER049_PDF, (4,)),
    utilatest.step(power.MASTER072_PDF, (1, 2)),
    utilatest.step(power.MASTER078_PDF, TEN),
    utilatest.step(power.MASTER083_PDF, TEN),
    utilatest.step(power.MASTER089_PDF, TEN),
    utilatest.step(power.MASTER098_PDF, TEN),
    utilatest.step(power.MASTER099B_PDF, (2,)),
    utilatest.step(power.MASTER099_PDF, TEN),
    utilatest.step(power.MASTER112_PDF, (5, 6)),
    utilatest.step(power.MASTER155_PDF, (1, 2)),
    utilatest.step(power.MASTER193_PDF, (3, 4, 5)),
    utilatest.step(power.PAPER14B_PDF, (1,)),
])
@utilatest.nightly
def test_toc_validate(source, pages, mp, td):
    """Verify parsing behavior and check that toc is located
    automatically in range of `TEN` pages."""
    utilatest.fixture_requires(source)
    pages = utila.from_tuple(pages, ',') if pages else ':'
    Evaluate(source, pages, td.tmpdir, mp).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, workdir, mp):
        super().__init__(
            program=functools.partial(
                tests.run,
                mp=mp,
            ),
            step='toc',
            source=source,
            pages=pages,
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.load_toc,
        )

    def load_toc(self, _):  # pylint:disable=W0613
        path = reftable.path.toc(self.workdir)
        loaded = serializeraw.load_toc(path)
        return loaded

    def raw(self, value) -> str:
        result = []
        for item in value:
            result.extend(self.recursive(item, level=0))
        titles = utila.NEWLINE.join(result)
        return titles

    def recursive(self, item, level):
        result = ['    ' * level + item.title]
        assert item.raw_location >= 0, str(item)
        if not item.children:
            return result
        for child in item.children:
            result.extend(self.recursive(child, level + 1))
        return result


@pytest.mark.parametrize('source,pages', [
    utilatest.step(power.BACHELOR063_PDF, TEN),
    utilatest.step(power.BACHELOR076_PDF, TEN),
    utilatest.step(power.BACHELOR090_PDF, TEN),
    utilatest.step(power.BACHELOR101_PDF, (1, 2)),
    utilatest.step(power.BACHELOR111_PDF, TEN),
    utilatest.step(power.BACHELOR128_PDF, (3, 4, 5)),
    utilatest.step(power.BACHELOR241_PDF, (4, 5, 6, 7)),
    utilatest.step(power.DISS143_PDF, TEN),
    utilatest.step(power.DISS157_PDF, (6, 7, 8)),
    utilatest.step(power.DISS172_PDF, TEN),
    utilatest.step(power.DISS180_PDF, (4, 5)),
    utilatest.step(power.HOME050_PDF, (3, 4)),
    utilatest.step(power.MASTER049_PDF, (4,)),
    utilatest.step(power.MASTER072_PDF, (1, 2)),
    utilatest.step(power.MASTER078_PDF, (2, 3, 4)),
    utilatest.step(power.MASTER083_PDF, TEN),
    utilatest.step(power.MASTER089_PDF, (1,)),
    utilatest.step(power.MASTER098_PDF, TEN),
    utilatest.step(power.MASTER099_PDF, TEN),
    utilatest.step(power.MASTER110_PDF, TEN),
    utilatest.step(power.MASTER127_PDF, TEN),
    utilatest.step(power.MASTER155_PDF, (1, 2)),
    utilatest.step(power.MASTER193_PDF, (2, 3, 4)),
    utilatest.step(power.PAPER14B_PDF, (1,)),
])
@utilatest.longrun
def test_toc_style_numbered(source, pages):
    current = tocstyle_frompath(source, pages)
    assert current == iamraw.TocStyle.NUMBERED


@pytest.mark.parametrize('source,pages', [
    utilatest.step(power.DISS406_PDF, (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)),
])
@utilatest.longrun
def test_toc_style_stepped(source, pages):
    current = tocstyle_frompath(source, pages)
    assert current == iamraw.TocStyle.STEPPED


@pytest.mark.parametrize('source,pages', [
    utilatest.step(power.MASTER099B_PDF, (2,)),
])
@utilatest.longrun
def test_toc_style_sectioned(source, pages):
    current = tocstyle_frompath(source, pages)
    assert current == iamraw.TocStyle.SECTIONED


def tocstyle_frompath(source, pages):
    utilatest.fixture_requires(source)
    source = power.link(source)
    ptcn = serializeraw.ptcn_frompath(
        source,
        prefix='oneline',
        pages=pages,
    )
    extracted = reftable.toc.run.extract(ptcn)
    extracted = utila.flatten(extracted)
    current = elements.toc_style(extracted)
    return current
