# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import reftable.abbrev
import reftable.abbrev.parser


def work(
    text: str,
    textposition: str,
    text_oneline: str,
    textposition_oneline: str,
    headerfooter: str,
    sizeandborder: str,
    pages: tuple = None,
) -> str:
    data = load_data(
        text,
        textposition,
        text_oneline,
        textposition_oneline,
        headerfooter,
        sizeandborder,
        pages,
    )
    parsed = reftable.abbrev.parser.parse(data)
    # dump result
    dumped = serializeraw.dump_abbreviation_table(parsed)
    return dumped


def load_data(
    text: str,
    textposition: str,
    text_oneline: str,
    textposition_oneline: str,
    headerfooter: str,
    sizeandborder: str,
    pages: tuple = None,
) -> reftable.abbrev.AbbreviationData:
    normal = serializeraw.ptcn_fromfile(
        text=text,
        textpositions=textposition,
        sizeandborder=sizeandborder,
        headerfooter=headerfooter,
        pages=pages,
    )
    oneline = serializeraw.ptcn_fromfile(
        text=text_oneline,
        textpositions=textposition_oneline,
        sizeandborder=sizeandborder,
        headerfooter=headerfooter,
        pages=pages,
    )
    data = reftable.abbrev.AbbreviationData(
        normal=normal,
        oneline=oneline,
    )
    return data
