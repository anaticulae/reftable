# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import reftable.toc

CONTENT = """
5.1.5 Präsentationsschicht . . . . . . . . . . . . . . . . . . . 58
6 Evaluierung und Demonstration des Prototypen 62
6.1 Evaluierung des Systems . . . . . . . . . . . . . . . . . . . . . 62
6.1.1 Modularit3t und Erweiterbarkeit . . . . . . . . . . . . 62
6.1.2 Funktionalität und Benutzbarkeit . . . . . . . . . . . . 63
6.2 Demonstration des Prototypen . . . . 66
6.2.1 Anwendungsstart und Konfiguration eines Projektes . . 66
6.2.2 Auswahl von Projekten und KNX-Gruppen . . . . . . . 69
6.2.3 Steuern und Überwachen von KNX-Geräten . . . . . . 71
7 Zusammenfassung und Ausblick 76
7.1 Zusammenfassung . . . . . . . . . . . . . . . . . . . . . . . . . 76
7.2 Ausblick . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 77
"""

HEADLINES = [
    reftable.toc.TocLine(
        level='6.1.2',
        title='Funktionalität und Benutzbarkeit',
        page='63',
        raw='6.1.2 Funktionalität und Benutzbarkeit . . . . . . . . . . . . 63',
    ),
    reftable.toc.TocLine(
        level='6.2',
        title='Demonstration des Prototypen',
        page='66',
        raw='6.2 Demonstration des Prototypen . . . . 66',
    ),
    reftable.toc.TocLine(
        level='6',
        title='Evaluierung und Demonstration des Prototypen',
        page='62',
        raw='6 Evaluierung und Demonstration des Prototypen 62',
    ),
    reftable.toc.TocLine(
        level='7',
        title='Zusammenfassung und Ausblick',
        page='76',
        raw='7 Zusammenfassung und Ausblick 76',
    ),
]


def test_toc_sort_byposition():
    """Avoid searching the subpattern, ensure that find finds the
    correct pattern in text.

    `Demonstration des Prototypen` is a substring of `Evaluierung und
    Demonstration des Prototypen` when using extracted title instead of
    extracted raw, the order of items is not sorted correctly cause the
    subpattern occurse before the whole text. (6.2.) / (6)
    """
    result = reftable.toc.sort_byposition(HEADLINES, CONTENT)
    pages = [item.page for item in result]
    assert utila.isascending(pages)
