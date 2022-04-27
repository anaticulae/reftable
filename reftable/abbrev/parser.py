# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import reftable.abbrev
import reftable.abbrev.geometry
import reftable.abbrev.simple

STRATEGIES = [
    reftable.abbrev.simple.SimpleAbbreviationParser,
    reftable.abbrev.geometry.GeometryAbbreviationParser,
]


def parse(data: reftable.abbrev.AbbreviationData) -> iamraw.AbbreviationResult:
    assert isinstance(data.normal, list), type(data)
    assert isinstance(data.oneline, list), type(data)

    parsed = [strategy(data).result() for strategy in STRATEGIES]

    judged = judge(parsed)
    return judged


def judge(results) -> iamraw.AbbreviationResult:
    simple = results[0]
    geometry = results[1]

    more_than_double_parsed = (len(geometry) * 2) < len(simple)
    if more_than_double_parsed:
        return simple
    return geometry
