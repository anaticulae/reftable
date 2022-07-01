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

ARCHIVE = utila.join(reftable.ROOT, 'tests/table/expected', exist=True)


#  TODO: IMPROVE PARSER A.10 and A.11 is not fully correct
@pytest.mark.parametrize('source, pages', [
    pytest.param(
        power.BACHELOR090_PDF,
        (9, 11),
        id='bachelor090',
    ),
    pytest.param(
        power.BACHELOR111_PDF,
        (98, 99),
        id='bachelor111',
    ),
])
@utilatest.nightly
def test_tabletable_validate(source, pages, testdir, monkeypatch):
    Evaluate(
        source=source,
        pages=utila.from_tuple(pages, separator=','),
        expected=utila.file_name(source),
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(tests.run, monkeypatch=monkeypatch),
            step='table',
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.load_tabletable,
            convert_source=False,
            index=expected,
        )

    def load_tabletable(self, _):  # pylint:disable=W0613
        path = reftable.path.table(self.workdir)
        loaded = serializeraw.load_toc(path)
        return loaded

    def raw(self, value) -> str:
        result = tables_raw(value)
        return result


def tables_raw(toc: iamraw.Toc) -> str:
    result = []

    def recursive(item, level):
        result = []
        result.append('    ' * level + item.title)
        assert item.raw_location >= 0, str(item)
        if item.children:
            for child in item.children:
                result.extend(recursive(child, level + 1))
        return result

    for item in toc:
        result.extend(recursive(item, level=0))
    titles = utila.NEWLINE.join(result)
    return titles
