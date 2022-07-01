# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import reftable
import tests

ARCHIVE = utila.join(reftable.ROOT, 'tests/abbrev/expected', exist=True)


@pytest.mark.parametrize('source, pages', [
    pytest.param(power.TECH019_PDF, 4, id='techo019'),
    pytest.param(power.BACHELOR090_PDF, (10, 11), id='bachelor090'),
])
def test_validate_abbrev(source, pages, testdir, monkeypatch):
    pages = utila.ensure_tuple(pages)
    Evaluate(
        source=source,
        pages=utila.from_tuple(pages, separator=','),
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(tests.run, monkeypatch=monkeypatch),
            step='abbrev',
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.load_table,
            convert_source=False,
        )

    def load_table(self, _):  # pylint:disable=W0613
        path = reftable.path.abbreviation(self.workdir)
        loaded = serializeraw.load_abbreviation_table(path)
        return loaded

    def raw(self, value: iamraw.AbbreviationResult) -> str:
        collected = []
        for item in value:
            line = f'{item.short:<15} {item.description}'
            collected.append(line)
        raw = utila.NEWLINE.join(collected)
        return raw
