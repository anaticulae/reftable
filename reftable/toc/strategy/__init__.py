# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import abc
import dataclasses
import typing

import elements.headline.lookup
import texmex
import utila

import reftable.toc
import reftable.toc.create


@dataclasses.dataclass
class ExtractionResult:
    content: list['TocLines'] = dataclasses.field(default_factory=list)
    invalid: list[typing.Any] = dataclasses.field(default_factory=list)
    strategy: str = None

    def __len__(self):
        return len(self.content)

    def __getitem__(self, index):
        return self.content[index]  # pylint:disable=E1136

    def __str__(self):
        collected = [str(self.strategy), 'VALID:']
        for item in utila.flat(self.content):
            collected.append(item.raw)
        if self.invalid:
            collected.append('INVALID:')
            for item in self.invalid:
                collected.append(item.raw)
        collected.append('')
        result = utila.NEWLINE.join(collected)
        return result


ExtractionResults = list[ExtractionResult]


class ExtractorStrategy(abc.ABC):

    def __init__(self, loaded: texmex.NavigatorMixins):
        self.loaded = loaded

    @abc.abstractmethod
    def result(self) -> ExtractionResult:
        pass

    def finalize_result(self, content):  # pylint:disable=R0201
        valids = remove_nonconnected_tocs(content)
        invalid_content = [item for item in content if item not in valids]
        extracted = group(
            valids,
            strategy=self.__class__.__name__,
        )
        content = extracted.content
        if too_many_dots_in_title(utila.flat(content)):
            utila.debug(f'too many dots in title: {self.__class__.__name__}')
            content = []
        result = ExtractionResult(
            content=content,
            invalid=invalid_content,
            strategy=self.__class__.__name__,
        )
        assert isinstance(result.content, list), type(result.content)
        return result


def group(extracted: reftable.toc.TocLines, strategy: str) -> ExtractionResult:
    right, invalid = utila.partition(
        key=lambda x: isinstance(x, reftable.toc.TocLine),
        items=extracted,
    )
    valid = remove_nonconnected_tocs(right)
    for item in right:
        if item not in valid:
            invalid.append(item)
    content = reftable.toc.create.groupby_chapter(valid)
    result = ExtractionResult(
        content=content,
        invalid=invalid,
        strategy=strategy,
    )
    return result


def remove_headline(
    content: texmex.PTN,
    headlines=None,
    count: int = 1,
) -> texmex.PTN:
    """Remove table of content headline to improve extraction result."""
    if not headlines:
        headlines = elements.headline.lookup.TOC
    result = content.hull_empty()
    for item in content:
        if count > 0 and utila.verysimilar(current=item.text, expected=headlines): # yapf:disable
            count -= 1
            continue
        result.insert(item.text, item.style, item.bounding)
    return result


def remove_nonconnected_tocs(items) -> list:
    """Ensure that toc is connected and not separated by whitepages.

    Select hugest group as single valid table of content.
    """
    if not items:
        return []
    pagenumbers = [item.pdfpage for item in items]
    pagenumbers = utila.groupby_diff(pagenumbers, sort=True, enlarge=True)
    valid_pages = utila.longest(pagenumbers, number=1)
    # remove non included items
    include = [item for item in items if item.pdfpage in valid_pages]
    return include


def too_many_dots_in_title(lines) -> bool:
    # TODO: HOLY VALUES
    numbers = len([line for line in lines if line.title.count('.') > 7])
    if numbers > 2:
        return True
    return False
