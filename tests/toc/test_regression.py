# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import reftable
import tests


@utilatest.requires(power.DISS157_PDF)
def test_appendix_level(td, mp):
    """Before this test, all appendix level where set to level 4."""
    source = power.link(power.DISS157_PDF)
    tests.run(
        f'--toc -i {source} -o {td.tmpdir}',
        mp=mp,
    )
    path = reftable.path.toc(td.tmpdir)
    loaded = serializeraw.load_toc(path)
    appendix = loaded.children[-2].children
    assert len(appendix) == 3
    levels = [item.level for item in appendix]
    assert levels == [2, 2, 2]
