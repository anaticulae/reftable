# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilotest


def headlines_frompath(path: str, pages=None):
    loaded = serializeraw.ptcn_frompath(
        path,
        pages=pages,
        prefix='oneline',
        validate_leftright=False,  # do not check writing text over border
    )
    return loaded


def master72_toc():
    utilotest.fixture_requires(hoverpower.MASTER072_PDF)
    return headlines_frompath(hoverpower.link(hoverpower.MASTER072_PDF),
                              pages=(1, 2))


def bachelor111_toc():
    utilotest.fixture_requires(hoverpower.BACHELOR111_PDF)
    return headlines_frompath(
        hoverpower.link(hoverpower.BACHELOR111_PDF),
        pages=(1, 2, 3, 4),
    )


def technical24_toc():
    utilotest.fixture_requires(hoverpower.TECH024_PDF)
    return headlines_frompath(hoverpower.link(hoverpower.TECH024_PDF),
                              pages=(1,))
