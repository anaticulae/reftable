# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import reftable.toc.basic.lineregex
import reftable.toc.create


def parse_group(items, page: int) -> reftable.toc.TocLines:
    assert page is not None, page
    parsed = [reftable.toc.basic.lineregex.parse(item.text) for item in items]
    matched = [item is not None for item in parsed]
    if all(matched):
        # all work is done
        parsed = set_pagelocation(parsed, page=page)
        return parsed
    result = []
    collected = []
    for match, item, parsed_item in zip(matched, items, parsed):
        if not match:
            collected.append(item)
            continue
        if collected:
            collected.append(item)
            extracted = group_collection_and_parse(collected)
            if extracted:
                result.append(extracted)
            else:
                # log not parsed
                utila.debug(f'could not group and parse {collected}')
            collected = []
            continue
        result.append(parsed_item)
    if collected:
        extracted = group_collection_and_parse(collected)
        if extracted:
            # parsing was successful
            result.append(extracted)
    result = set_pagelocation(result, page=page)
    return result


def set_pagelocation(
    items: reftable.toc.TocLines,
    page: int,
) -> reftable.toc.TocLines:
    # set parse page location
    for item in items:
        item.raw_location = page
    return items


def group_collection_and_parse(items):
    line = ' '.join([item.text for item in items])
    parsed = reftable.toc.basic.lineregex.parse(line)
    return parsed
