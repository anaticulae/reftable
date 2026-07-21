# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo


def abbreviation(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(path, 'reftable', 'abbrev_abbrev', prefix)


def toc(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(path, 'reftable', 'toc_toc', prefix)


def figure(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(path, 'reftable', 'figure_figure', prefix)


def table(path: str, prefix: str = '') -> str:
    return utilo.pathconnector(path, 'reftable', 'table_table', prefix)
