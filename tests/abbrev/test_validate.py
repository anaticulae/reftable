# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
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


@pytest.mark.parametrize('source', [
    pytest.param(power.TECH019_PDF, id='techo019'),
    pytest.param(power.BACHELOR090_PDF, id='bachelor090'),
])
def test_validate_abbrev(source, td, mp):
    utilatest.fixture_requires(source)
    pages = select_abbrev(source)
    if not pages:
        raise ValueError('no abbrev table found')
    Evaluate(
        source=source,
        pages=utila.from_tuple(pages, separator=','),
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, workdir, mp):
        super().__init__(
            program=functools.partial(tests.run, mp=mp),
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


def select_abbrev(source: str) -> tuple:
    # TODO: REPLACE WITH UTILA TEST CODE
    generated = power.link(source)
    sections = serializeraw.load_sections(generated)
    flat = utila.flatten_content(sections)
    pages = []
    for item in flat:
        if not isinstance(item, iamraw.sections.AbbreviationTable):
            continue
        pages.append(item.start)
    if not pages:
        return None
    result = tuple(pages)
    return result
