# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import reftable.feature.toc
import reftable.pageselector
import reftable.toc.create
import reftable.toc.strategy


@utilatest.requires(power.DOCU007_PDF)
def test_toc_groupby_level():
    navigators = serializeraw.create_pagetextcontentnavigators_frompath(
        power.link(power.DOCU007_PDF),
        prefix='oneline',
    )
    selected = reftable.pageselector.select_contentpages(navigators)
    # select toc pages only
    navigators = [item for item in navigators if item.page in selected]
    loaded = reftable.toc.strategy.ExtractionData(content=navigators)
    tableofcontent = reftable.toc.run.extract(loaded)

    tableofcontent = utila.flatten(tableofcontent.content)

    result = reftable.toc.create.groupby_level_numbered(tableofcontent)
    assert result
    dumped = serializeraw.dump_toc(result)
    assert dumped
    # TODO: Check level content


@pytest.mark.parametrize('resources, pages, expected', [
    pytest.param(
        power.DOCU027_PDF,
        (2,),
        13,
        id='docu027',
    ),
    pytest.param(
        power.DOCU007_PDF,
        (0,),
        12,
        marks=pytest.mark.xfail,
        id='simple',
    ),
    pytest.param(
        power.DOCU035_PDF,
        (5,),
        0,
        id='notoc',
    ),
    pytest.param(
        power.MASTER099B_PDF,
        (2,),
        14,
        id='master099b',
    ),
    pytest.param(
        power.BACHELOR037_PDF,
        (3, 4),
        47,
        id='bachelor037',
    ),
    pytest.param(
        power.BACHELOR241_PDF,
        (6,),
        35,
        id='bachelor241p6',
        marks=pytest.mark.xfail(reason='improve selector strategy'),
    ),
    pytest.param(
        power.BACHELOR241_PDF,
        (4,),
        25,
        id='bachelor241p4',
    ),
])
def test_extract_toc_from_path(resources, pages, expected):
    utilatest.fixture_requires(resources)
    resources = power.link(resources)
    navigators = serializeraw.create_pagetextcontentnavigators_frompath(
        path=resources,
        prefix='oneline',
        pages=pages,
    )
    loaded = reftable.toc.strategy.ExtractionData(content=navigators)
    extracted = reftable.toc.run.extract(
        loaded,
        min_detection_count=reftable.feature.toc.TOC_COUNT_MIN,
    )
    flat = utila.flatten(extracted)
    assert len(flat) == expected, str(flat)
