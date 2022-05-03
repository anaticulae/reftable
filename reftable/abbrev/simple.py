# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elements.headline.lookup
import iamraw
import utila

import reftable.abbrev


class SimpleAbbreviationParser(reftable.abbrev.AbbreviationExtractorStrategy):

    def result(self) -> iamraw.AbbreviationResult:
        ready = iamraw.AbbreviationResult()
        for page in self.loaded.oneline:
            parsed = parse_page(page)
            for item in parsed:
                ready.append(item)
        return ready


def parse_page(content):
    result = []
    for line in content:
        raw = line.text
        utila.debug(f'parse: {raw}')
        try:
            short, description = raw.split(maxsplit=1)
        except ValueError:
            if not isexcluded(raw):
                utila.debug(f'could not parse abbreviation: {raw}')
            continue
        if isexcluded(short) or isexcluded(description):
            utila.info(f'skip: {short}, {description}')
            continue
        short, description = short.strip(), description.strip()
        parsed = iamraw.Abbreviation(
            short=short,
            description=description,
        )
        utila.debug(f'parsed: {parsed}')
        result.append(parsed)
    return result


def isexcluded(item: str) -> bool:
    # TODO: ADD MORE SOPHISTICATED DOUBLE COLUMN CHECKER
    item = item.strip().lower()
    if item in elements.headline.lookup.HEADLINES:
        return True
    if item in NO_ABBREVIATION:
        return True
    return False


NO_ABBREVIATION = utila.splitlines("""\
BESCHREIBUNG
""")
