# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import copy
import math

import configo
import iamraw
import utila

ONELINE_MERGE_Y_DIFF_MAX = configo.HV_FLOAT_PLUS(default=5.0)


def oneline(page) -> str:
    """Improve parsed data from rawmaker to remove some little parsing
    problems as a result of bad pdf printing or text grouping.
    """
    if isinstance(page, iamraw.Page):
        lines = utila.flatten([
            container for container in page
            if isinstance(container, iamraw.TextContainer)
        ])
        # lines = oneline_merge(lines)
        # TODO: CHECK FOR ONELINE_MERGE
    else:
        # PageTextNavigator
        lines = oneline_merge(page[:])
    lines = [item.text for item in lines]
    lines = split_newlines(lines)
    lines = [item.strip() for item in lines]
    # remove single word line
    # HOMEWORK PAGE 4, remove `Inhaltsverzeichnis` in header.
    # # TODO: Look for a better header exclusion strategy
    # TODO: ONLY REQUIRED IF TO FEW PAGES ARE AVAILABLE, CAUSE HEADER
    # FOOTER STRATEGY NEEDS SOME DATA
    # TODO: THINK ABOUT REMOVING THIS
    lines = [item for item in lines if len(item.split()) > 1]
    text = utila.NEWLINE.join(lines)
    return text


def oneline_merge(lines: list) -> list:
    """Merge layout if required."""
    # TODO: EXPERIMENTAL: IMPROVE, MOVE TO RAWMAKER?
    if not lines:
        return []
    # TODO: REPLACE BY .copy
    lines = [copy.deepcopy(item) for item in lines]
    # left to right
    lines = sorted(lines, key=lambda item: item.bounding.x0)
    # top to down
    lines = sorted(lines, key=lambda item: item.bounding.y0)
    result = [lines[0]]
    for item in lines[1:]:
        last_y = result[-1].bounding.y0
        current_y = item.bounding.y0
        if math.fabs(last_y - current_y) > ONELINE_MERGE_Y_DIFF_MAX:
            result.append(item)
            continue
        # TODO: MERGE BOUNDING
        # merge
        # do NOT strip second item, we do not want to lose the newline
        result[-1].text = result[-1].text.strip() + ' ' + item.text
    return result


def split_newlines(items):
    result = []
    for item in items:
        result.extend(item.splitlines())
    return result
