# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import reftable.figure.column
import reftable.figure.normal
import reftable.toc.create


def run(
    text: str,
    textpositions: str,
    oneline_text: str,
    oneline_textpositions: str,
    headerfooter: str,
    sizeandborder: str,
    pages: tuple = None,
):
    oneline = serializeraw.create_pagetextcontentnavigators_fromfile(
        oneline_text,
        oneline_textpositions,
        sizeandborder=sizeandborder,
        headerfooter=headerfooter,
        pages=pages,
    )
    result = reftable.figure.normal.run(oneline)
    if not result:
        ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
            text,
            textpositions,
            sizeandborder=sizeandborder,
            headerfooter=headerfooter,
            pages=pages,
        )
        result = reftable.figure.column.run(ptcns)
    result = reftable.toc.create.groupby_level(result)  # pylint:disable=R0204
    return result
