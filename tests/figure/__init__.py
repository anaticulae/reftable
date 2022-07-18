# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import reftable
import tests


def extract_table(source, pages, mp, td):
    pages = ','.join((str(item) for item in pages)) if pages else ''
    pages = f'--pages={pages}' if pages else ''
    cmd = f'-i {source} --table {pages}'
    tests.run(cmd, mp=mp)
    path = reftable.path.table(td.tmpdir)
    table = serializeraw.load_toc(path)
    return table
