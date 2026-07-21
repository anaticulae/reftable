# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import elementae
import hoverpower
import iamraw
import pytest
import resinf
import serializeraw
import utilo
import utilotest

import reftable
import reftable.toc.run
import reftable.toc.strategy
import tests

ARCHIVE = utilo.join(reftable.ROOT, 'tests/toc/expected', exist=True)
TEN = utilo.make_tuple(10)


@pytest.mark.parametrize('source, pages', [
    utilotest.step(hoverpower.BACHELOR028_PDF, (1,)),
    utilotest.step(hoverpower.BACHELOR032A_PDF, (1,)),
    utilotest.step(hoverpower.BACHELOR032_PDF, (1,)),
    utilotest.step(hoverpower.BACHELOR039_PDF, (1,)),
    utilotest.step(hoverpower.BACHELOR041A_PDF, (1,)),
    utilotest.step(hoverpower.BACHELOR063_PDF, TEN),
    utilotest.step(hoverpower.BACHELOR076_PDF, TEN),
    utilotest.step(hoverpower.BACHELOR078_PDF, (1,)),
    utilotest.step(hoverpower.BACHELOR086_PDF, (1,)),
    utilotest.step(hoverpower.BACHELOR090_PDF, TEN),
    utilotest.step(hoverpower.BACHELOR101_PDF, (1, 2)),
    utilotest.step(hoverpower.BACHELOR105_PDF, (1, 2)),
    utilotest.step(hoverpower.BACHELOR111_PDF, (1, 2, 3, 4)),
    utilotest.step(hoverpower.BACHELOR128_PDF, (3, 4, 5)),
    utilotest.step(hoverpower.BACHELOR241_PDF, (4, 5, 6, 7)),
    utilotest.step(hoverpower.BOOK173_PDF, (9, 10, 11, 12)),
    utilotest.step(hoverpower.DISS154_PDF, (4, 5, 6, 7)),
    utilotest.step(hoverpower.DISS157_PDF, (6, 7, 8)),
    utilotest.step(hoverpower.DISS172_PDF, (7, 8)),
    utilotest.step(hoverpower.DISS178_PDF, (3, 4)),
    utilotest.step(hoverpower.DISS180_PDF, (4, 5)),
    utilotest.step(hoverpower.DISS406_PDF,
                   (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)),
    utilotest.step(hoverpower.DISS480_PDF, (2, 3)),
    # utilotest.step(hoverpower.HC_DISS128, (6, 7)),
    # utilotest.step(hoverpower.HC_DISS148, (6, 7)),
    # utilotest.step(hoverpower.HC_DISS166, (6, 7)),
    # utilotest.step(hoverpower.HC_DISS171, (8, 9, 10)),
    # utilotest.step(hoverpower.HC_DISS193, (9, 10, 11, 12)),
    utilotest.step(hoverpower.HOME007_PDF, (0,)),
    utilotest.step(hoverpower.HOME012_PDF, (1,)),
    utilotest.step(hoverpower.HOME014B_PDF, (1,)),
    utilotest.step(hoverpower.HOME014C_PDF, (1,)),
    utilotest.step(hoverpower.HOME014_PDF, (1,)),
    utilotest.step(hoverpower.HOME015_PDF, (1,)),
    utilotest.step(hoverpower.HOME016_PDF, (1,)),
    utilotest.step(hoverpower.HOME017C_PDF, (1,)),
    utilotest.step(hoverpower.HOME018_PDF, (2,)),
    utilotest.step(hoverpower.HOME019A_PDF, (1,)),
    utilotest.step(hoverpower.HOME019B_PDF, (1,)),
    utilotest.step(hoverpower.HOME019_PDF, (1,)),
    utilotest.step(hoverpower.HOME020_PDF, (1,)),
    utilotest.step(hoverpower.HOME021A_PDF, (1,)),
    utilotest.step(hoverpower.HOME021B_PDF, (1,)),
    utilotest.step(hoverpower.HOME021_PDF, (0, 1)),
    utilotest.step(hoverpower.HOME022A_PDF, (1,)),
    utilotest.step(hoverpower.HOME022_PDF, (1,)),
    utilotest.step(hoverpower.HOME050_PDF, (3, 4)),
    utilotest.step(hoverpower.MASTER049_PDF, (4,)),
    utilotest.step(hoverpower.MASTER072_PDF, (1, 2)),
    utilotest.step(hoverpower.MASTER078_PDF, TEN),
    utilotest.step(hoverpower.MASTER083_PDF, TEN),
    utilotest.step(hoverpower.MASTER089_PDF, TEN),
    utilotest.step(hoverpower.MASTER098_PDF, TEN),
    utilotest.step(hoverpower.MASTER099B_PDF, (2,)),
    utilotest.step(hoverpower.MASTER099_PDF, TEN),
    utilotest.step(hoverpower.MASTER112_PDF, (5, 6)),
    utilotest.step(hoverpower.MASTER155_PDF, (1, 2)),
    utilotest.step(hoverpower.MASTER193_PDF, (3, 4, 5)),
    utilotest.step(hoverpower.PAPER14B_PDF, (1,)),
])
@utilotest.nightly
def test_toc_validate(source, pages, mp, td):
    """Verify parsing behavior and check that toc is located
    automatically in range of `TEN` pages."""
    if not utilo.exists(resinf.link(source)):
        # TODO: VERIFY WHY FIXTURE_REUQIRES DOES OT WORK
        pytest.skip(reason='generate source')
    utilotest.fixture_requires(source)
    pages = utilo.from_tuple(pages, ',') if pages else ':'
    Evaluate(source, pages, td.tmpdir, mp).evaluate()


class Evaluate(utilotest.BaseLiner):

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
        titles = utilo.NEWLINE.join(result)
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
    utilotest.step(hoverpower.BACHELOR063_PDF, TEN),
    utilotest.step(hoverpower.BACHELOR076_PDF, TEN),
    utilotest.step(hoverpower.BACHELOR090_PDF, TEN),
    utilotest.step(hoverpower.BACHELOR101_PDF, (1, 2)),
    utilotest.step(hoverpower.BACHELOR111_PDF, TEN),
    utilotest.step(hoverpower.BACHELOR128_PDF, (3, 4, 5)),
    utilotest.step(hoverpower.BACHELOR241_PDF, (4, 5, 6, 7)),
    utilotest.step(hoverpower.DISS143_PDF, TEN),
    utilotest.step(hoverpower.DISS157_PDF, (6, 7, 8)),
    utilotest.step(hoverpower.DISS172_PDF, TEN),
    utilotest.step(hoverpower.DISS180_PDF, (4, 5)),
    utilotest.step(hoverpower.HOME050_PDF, (3, 4)),
    utilotest.step(hoverpower.MASTER049_PDF, (4,)),
    utilotest.step(hoverpower.MASTER072_PDF, (1, 2)),
    utilotest.step(hoverpower.MASTER078_PDF, (2, 3, 4)),
    utilotest.step(hoverpower.MASTER083_PDF, TEN),
    utilotest.step(hoverpower.MASTER089_PDF, (1,)),
    utilotest.step(hoverpower.MASTER098_PDF, TEN),
    utilotest.step(hoverpower.MASTER099_PDF, TEN),
    utilotest.step(hoverpower.MASTER110_PDF, TEN),
    utilotest.step(hoverpower.MASTER127_PDF, TEN),
    utilotest.step(hoverpower.MASTER155_PDF, (1, 2)),
    utilotest.step(hoverpower.MASTER193_PDF, (2, 3, 4)),
    utilotest.step(hoverpower.PAPER14B_PDF, (1,)),
])
@utilotest.longrun
def test_toc_style_numbered(source, pages):
    current = tocstyle_frompath(source, pages)
    assert current == iamraw.TocStyle.NUMBERED


@pytest.mark.parametrize('source,pages', [
    utilotest.step(hoverpower.DISS406_PDF,
                   (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)),
    utilotest.step(hoverpower.HOME021_PDF, (0, 1)),
])
@utilotest.longrun
def test_toc_style_stepped(source, pages):
    current = tocstyle_frompath(source, pages)
    assert current == iamraw.TocStyle.STEPPED


@pytest.mark.parametrize('source,pages', [
    utilotest.step(hoverpower.MASTER099B_PDF, (2,)),
])
@utilotest.longrun
def test_toc_style_sectioned(source, pages):
    current = tocstyle_frompath(source, pages)
    assert current == iamraw.TocStyle.SECTIONED


def tocstyle_frompath(source, pages):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    ptcn = serializeraw.ptcn_frompath(
        source,
        prefix='oneline',
        pages=pages,
    )
    extracted = reftable.toc.run.extract(ptcn)
    extracted = utilo.flat(extracted)  # pylint:disable=R0204
    current = elementae.toc_style(extracted)
    return current
