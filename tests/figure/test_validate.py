# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import iamraw
import pytest
import serializeraw
import utilo
import utilotest

import reftable
import tests

ARCHIVE = utilo.join(reftable.ROOT, 'tests/figure/expected', exist=True)


@pytest.mark.parametrize(
    'source, pages',
    [
        pytest.param(
            hoverpower.BACHELOR090_PDF,
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
            id='bachelor090',
        ),
        pytest.param(
            hoverpower.BACHELOR037_PDF,
            (0, 1, 2, 3, 4),
            id='bachelor037',
        ),
        # pytest.param(
        #     hoverpower.BACHELOR063_PDF,
        #     (59, 60, 61, 62),
        #     id='bachelor063',
        # ),
        # pytest.param(
        #     hoverpower.MASTER075_PDF,
        #     (71, 72),
        #     id='master075',
        # ),
        pytest.param(
            hoverpower.BACHELOR111_PDF,
            (94, 95, 96),
            id='bachelor111',
        ),
    ])
@utilotest.nightly
def test_table_validate(source, pages, td, mp):
    utilotest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=utilo.from_tuple(pages, separator=','),
        expected=utilo.file_name(source),
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilotest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, mp):
        super().__init__(
            program=functools.partial(tests.run, mp=mp),
            step='figure',
            pages=pages,
            source=hoverpower.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.load_table,
            convert_source=False,
            index=expected,
        )

    def load_table(self, _):  # pylint:disable=W0613
        path = reftable.path.figure(self.workdir)
        loaded = serializeraw.load_toc(path)
        return loaded

    def raw(self, value) -> str:
        result = figures_raw(value)
        return result


def figures_raw(toc: iamraw.Toc) -> str:
    result = []

    def recursive(item, level) -> list:
        result = []
        result.append('    ' * level + item.title)
        assert item.raw_location >= 0, str(item)
        if item.children:
            for child in item.children:
                result.extend(recursive(child, level + 1))
        return result

    for item in toc:
        result.extend(recursive(item, level=0))
    raw = utilo.NEWLINE.join(result)
    return raw
