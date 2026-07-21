# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import reftable.feature.toc
import reftable.pageselector
import reftable.toc.create
import reftable.toc.strategy


@utilotest.requires(hoverpower.DOCU007_PDF)
def test_toc_groupby_level():
    navigators = serializeraw.ptcn_frompath(
        hoverpower.link(hoverpower.DOCU007_PDF),
        prefix='oneline',
    )
    selected = reftable.pageselector.select_contentpages(navigators)
    # select toc pages only
    navigators = [item for item in navigators if item.page in selected]
    tableofcontent = reftable.toc.run.extract(navigators)
    tableofcontent = utilo.flat(tableofcontent.content)  # pylint:disable=R0204
    result = reftable.toc.create.groupby_level_numbered(tableofcontent)
    assert result
    dumped = serializeraw.dump_toc(result)
    assert dumped
    # TODO: Check level content


@pytest.mark.parametrize('resources, pages, expected', [
    pytest.param(
        hoverpower.DOCU027_PDF,
        (2,),
        13,
        id='docu027',
    ),
    pytest.param(
        hoverpower.DOCU007_PDF,
        (0,),
        12,
        marks=pytest.mark.xfail,
        id='simple',
    ),
    pytest.param(
        hoverpower.DOCU035_PDF,
        (5,),
        0,
        id='notoc',
    ),
    pytest.param(
        hoverpower.MASTER099B_PDF,
        (2,),
        14,
        id='master099b',
    ),
    pytest.param(
        hoverpower.BACHELOR037_PDF,
        (3, 4),
        47,
        id='bachelor037',
    ),
    pytest.param(
        hoverpower.BACHELOR241_PDF,
        (6,),
        35,
        id='bachelor241p6',
        marks=pytest.mark.xfail(reason='improve selector strategy'),
    ),
    pytest.param(
        hoverpower.BACHELOR241_PDF,
        (4,),
        25,
        id='bachelor241p4',
    ),
])
def test_extract_toc_from_path(resources, pages, expected):
    utilotest.fixture_requires(resources)
    resources = hoverpower.link(resources)
    navigators = serializeraw.ptcn_frompath(
        path=resources,
        prefix='oneline',
        pages=pages,
    )
    extracted = reftable.toc.run.extract(
        navigators,
        min_detection_count=reftable.feature.toc.TOC_COUNT_MIN,
    )
    flat = utilo.flat(extracted)
    assert len(flat) == expected, str(flat)
