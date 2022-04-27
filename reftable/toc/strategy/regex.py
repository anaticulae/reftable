# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""toc - regex extractor
=====================

Extract headlines based on regex pattern.

design decision
---------------

Should we support following whitespaces?

    It is not required to support lines with ending whitespaces. Following
    whitespace puts water into the wine and leads to more missmatchings. The
    better approach is to improve the pdf-parser to avoid following
    whitespaces.

    See: :class:`tests.toc.test_regex.test_extract_toc_line_whitespace_decission`.
"""

import re

import configo
import iamraw
import utila

import reftable.toc
import reftable.toc.basic.layout
import reftable.toc.basic.lineregex
import reftable.toc.strategy

TOC_LINE_LENGTH_MAX = configo.HV_INT_PLUS(default=250)

TOC_LINE_LENGTH_MIN = configo.HV_INT_PLUS(default=9)


class RegexTocExtractor(reftable.toc.strategy.ExtractorStrategy):

    def result(self) -> reftable.toc.strategy.ExtractionResult:
        content = self.loaded.content
        if content:
            # TODO: RUN THIS FOR OTHER PAGES THAN THE FIRST ONE?
            content[0] = reftable.toc.strategy.remove_headline(content[0])
        parsed = [parse_page(page) for page in self.loaded.content]
        flat = utila.flatten(parsed)
        grouped = reftable.toc.strategy.group(
            flat,
            strategy=self.__class__.__name__,
        )
        return grouped


def parse_page(page: iamraw.Page) -> reftable.toc.TocLines:
    """Merge `page` to raw string and extract the lines of table of content.

    Hint:
        see `parse`
    """
    # prepare data
    text: str = reftable.toc.basic.layout.oneline(page)
    # run extraction
    result = parse(text)
    # setup parse page location
    for item in result:
        item.raw_location = page.page
    return result


def parse(content: str) -> reftable.toc.TocLines:
    """Parse table of content via regex.

    Args
        content(str): content of block of text
    Returns:
        ordered list form top to down of parse table of content
    Pattern:

        with level:

        .. code-block :: none

            X.      Chapter ........... 1
            X.X     Section . . . . . . 3

        or no level:

        .. code-block :: none

            Eidesstattliche Erklärung ........... 69

    Regression test that this example last very long.
    >>> parse('35689101315161819202325262829303132331247111214172122242')
    []
    """
    duplicated = content
    result = []
    for pattern in [
            reftable.toc.basic.lineregex.EXTENDED_PATTERN,
            reftable.toc.basic.lineregex.EXTENDED_PATTERN_LETTER,
            reftable.toc.basic.lineregex.DICTIONARY,
            reftable.toc.basic.lineregex.NO_LEVEL,
            reftable.toc.basic.lineregex.NO_DOTS,
    ]:
        for line in re.finditer(pattern, content):
            item = reftable.toc.basic.lineregex.extract_match(line)
            if len(item.raw) < TOC_LINE_LENGTH_MIN:
                utila.debug(f'toc line too short: {item.raw}')
                # TODO: REMOVE HACK LATER
                continue
            result.append(item)
            # remove already matched content to do not confuse lower
            # strict pattern
            # TODO: INVESTIGATE TO GHOST PATTERN?
            content = content.replace(item.raw, '')
    nolevels = parse_nolevel(content)
    result.extend(nolevels)
    # remove duplications, which can occur when table of content is on the
    # same page as first headline.
    result = reftable.toc.remove_duplication(result)
    # TODO: MOVE THIS TO LINE -15???
    # remove long lines which can not be real lines
    result = [item for item in result if len(item.title) < TOC_LINE_LENGTH_MAX]
    # Ensure that toc list is ordered by position on pdf page
    result = reftable.toc.sort_byposition(result, duplicated)
    return result


def parse_nolevel(content: str) -> list:
    r"""\
    >>> parse_nolevel(' 1.2.3 Register .... 10\n  Quellenverzeichnis .... 23')
    [TocLine(level=None, title='Quellenverzeichnis', page='23'...)]
    """
    result = []
    # TODO: improve this
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.match(r'^\d', line):
            continue
        matched = re.match(reftable.toc.basic.lineregex.NO_LEVEL, line)
        if not matched:
            continue
        matched = reftable.toc.basic.lineregex.extract_match(matched)
        result.append(matched)
    return result
