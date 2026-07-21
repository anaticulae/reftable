# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import serializeraw
import utilotest

import reftable.feature.abbrev


@utilotest.longrun
@utilotest.requires(hoverpower.BACHELOR037_PDF)
def test_abbreviation_work():
    source = hoverpower.link(hoverpower.BACHELOR037_PDF)

    text = iamraw.path.text(source)
    textposition = iamraw.path.textposition(source)

    oneline_text = iamraw.path.text(source, prefix='oneline')
    oneline_textposition = iamraw.path.textposition(source, prefix='oneline')

    headerfooter = iamraw.path.headerfooters(source)
    sizeandborder = iamraw.path.sizeandborder(source)

    dumped = reftable.feature.abbrev.work(
        text,
        textposition,
        oneline_text,
        oneline_textposition,
        headerfooter,
        sizeandborder,
        pages=(1,),
    )

    loaded = serializeraw.load_abbreviation_table(dumped)
    assert len(loaded) == 26
