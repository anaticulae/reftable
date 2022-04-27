# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation
============

Examples:

* homework/page_50_math.pdf:page6
* master/page_116_images_toc_formular.pdf:95

TODO: Abbreviation creation tool
TODO: Symbol collector
"""

import abc
import dataclasses

import iamraw
import texmex


@dataclasses.dataclass
class AbbreviationData:
    normal: texmex.PageTextNavigators = None
    oneline: texmex.PageTextNavigators = None


class AbbreviationExtractorStrategy(abc.ABC):

    def __init__(self, loaded: AbbreviationData):
        self.loaded = loaded

    @abc.abstractmethod
    def result(self) -> iamraw.AbbreviationResult:
        pass
