# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw.path
import pytest
import serializeraw
import utilo
import utilotest

import reftable.feature.toc
import reftable.toc.basic.lineregex
import reftable.toc.strategy.regex as gtsr


@utilotest.longrun
@utilotest.requires(hoverpower.MASTER072_PDF)
def test_extract_toc_from_master_pages72_page_1and2():
    master72_text = iamraw.path.text(
        hoverpower.link(hoverpower.MASTER072_PDF),
        prefix='oneline',
    )
    document = serializeraw.load_document(master72_text)
    page1, page2 = document[1:3]
    result_page1 = gtsr.parse_page(page1)
    assert len(result_page1) == 23
    assert all(not '...' in item.title for item in result_page1)
    result_page2 = gtsr.parse_page(page2)
    assert len(result_page2) == 9
    assert all(not '...' in item.title for item in result_page2)


FIRST_LINE = ('2.1 Web 2.0, Social Web und Social Media: '
              'Abgrenzungen und Definitionen   .............. 4')

SECOND_LINE = (
    '2.   Das Social Web und die Privatsphäre Selbstdarstellungsverhalten\n'
    'der Nutzer aus Sicht von Massenmedien und Literatur .... 4')

# TODO: INVESTIGATE IN FOLLOWING `    ` Whitespaces
# TODO: FIX REGEX_PATTERN


@pytest.mark.parametrize('content, expected', [
    pytest.param(
        FIRST_LINE,
        [
            reftable.toc.TocLine(
                '2.1',
                'Web 2.0, Social Web und Social Media: Abgrenzungen und Definitionen',
                '4',
                FIRST_LINE,
            ),
        ],
        id='first_line',
    ),
    pytest.param(
        SECOND_LINE,
        [
            reftable.toc.TocLine(
                level='2.',
                title=
                ('Das Social Web und die Privatsphäre Selbstdarstellungsverhalten '
                 'der Nutzer aus Sicht von Massenmedien und Literatur'),
                page='4',
                raw=SECOND_LINE,
            )
        ],
        id='second_line',
    )
])
def test_extract_toc_line(content, expected):
    parsed = gtsr.parse(content)
    assert parsed == expected, str(parsed)


def test_extract_toc_line_whitespace_decision():
    """See design decission: We do not want to support following whitespaces."""

    text = '2. We do not want whitespaces at the end ......... 4     '
    parsed = gtsr.parse(text)
    assert not parsed, 'we do not want to support whitespaces'

    text = '       2. We do not want whitespaces at the end ......... 4'
    parsed = gtsr.parse(text)
    assert not parsed, 'we do not want to support whitespaces'

    text = '       2. We do not want whitespaces at the end ......... 4   '
    parsed = gtsr.parse(text)
    assert not parsed, 'we do not want to support whitespaces'


def test_toc_lineregex_parse():
    line = '2.2.3 Drahtlostechnologien fuer Nahbereichsnetzwerke (WPAN) 15'
    parsed = reftable.toc.basic.lineregex.parse(line)
    assert parsed.level == '2.2.3'
    assert parsed.title == 'Drahtlostechnologien fuer Nahbereichsnetzwerke (WPAN)'
    assert parsed.page == '15'


EXAMPLES = """\
1 Einleitung ..................................................... 1
1 Einleitung 1

3 Der Elysée-Vertrag – Ein deutsch-französischer Erinnerungsort ............ 25
3 Der Elysée-Vertrag – Ein deutsch-französischer Erinnerungsort 25

7.2 Tabellenverzeichnis ................................... 94
7.2 Tabellenverzeichnis 94

5.6 Reflexion der kulturdidaktischen Lernziele ................ 82
5.6 Reflexion der kulturdidaktischen Lernziele 82

2. Sänger der Gegenwart:\nAudiovisuelle Medien im Zeichen formaler Kontinuität.................5
2. Sänger der Gegenwart: Audiovisuelle Medien im Zeichen formaler Kontinuität 5

Anhang A: Die Reise des Helden, in der Odyssee...............................82
Anhang%20A: Die Reise des Helden, in der Odyssee 82

Literaturverzeichnis........................................................71
_ Literaturverzeichnis 71

7.4.2. Interpretation der; Ergebnisse der nach Mayring?....................... 77
7.4.2. Interpretation der; Ergebnisse der nach Mayring? 77

4.1.1. Selbstbeobachtung................................................... 37
4.1.1. Selbstbeobachtung 37

Abkürzungsverzeichnis…………………………………5
_ Abkürzungsverzeichnis 5

8. Beantwortung der Forschungsfragen und\nweiterführende Fragen ........................ 80
8. Beantwortung der Forschungsfragen und weiterführende Fragen 80

7. Zusammenfassung und Ausblick 80
7. Zusammenfassung und Ausblick 80

A. Anhang                 XXI
A. Anhang XXI

2. Das Social –\nSelbstdarstellungsverhalten  ....  4
2. Das Social – Selbstdarstellungsverhalten 4

Eidesstattliche Erklärung .................................................. 69
_ Eidesstattliche Erklärung 69

7.4.1. Interpretation Konsumtagebücher Auswertung .......................... 66
7.4.1. Interpretation Konsumtagebücher Auswertung 66

Literatur- und Quellenverzeichnis ........................................ 85
_ Literatur- und Quellenverzeichnis 85

A.4.3 Gearbeitet in SOLAR I und/oder SOLAR II (unabhängig von der\nAnzahl der Wochenstunden) . . . . . . . . . . . . . . . . . . . . . . 134
A.4.3 Gearbeitet in SOLAR I und/oder SOLAR II (unabhängig von der Anzahl der Wochenstunden) 134

B Alle Abbildungen zum Vergleich der Parameterschätzer 14
B Alle Abbildungen zum Vergleich der Parameterschätzer 14

C R-Code 161
C R-Code 161

A.6.2 Kurzbeschreibung der aus der Basis-Job-Matrix gebildeten Variablen 146
A.6.2 Kurzbeschreibung der aus der Basis-Job-Matrix gebildeten Variablen 146"""

EXAMPLES = [
    pytest.param(item, id=f'{index}')
    for index, item in enumerate(EXAMPLES.split('\n\n'))
]


@pytest.mark.parametrize('resources', EXAMPLES)
def test_parse_line(resources):
    line, expected = resources.rsplit('\n', maxsplit=1)

    expected_level, expected = expected.split(maxsplit=1)
    if expected_level == '_':
        expected_level = None
    else:
        expected_level = expected_level.replace('%20', ' ')

    expected_title, expected_page = expected.rsplit(maxsplit=1)

    parsed = gtsr.parse(line)
    assert len(parsed) == 1, str(parsed)
    parsed = parsed[0]

    parsed_title = parsed.title.replace('\n', ' ')
    assert parsed.level == expected_level, parsed
    assert parsed.page == expected_page, parsed
    assert parsed_title == expected_title, parsed


CONTENT = """\
7.3.  Qualitative Sozialforschung ........................................... 60
7.4. Interpretation der Ergebnisse ......................................... 65
7.4.1. Interpretation der Ergebnisse der Konsumtagebuecher anhand der quantitativen
Auswertung durch statistische Daten ........................................ 66
7.4.2. Interpretation der Ergebnisse der Frageboegen anhand der qualitativen Auswertung
durch die qualitative Inhaltsanalyse nach Mayring........................... 77

8.  Beantwortung der Forschungsfragen und Hypothesen sowie Fazit und
weiterführende Fragen ...................................................... 80
Literatur- und Quellenverzeichnis .......................................... 85
Abbildungs- und Tabellenverzeichnis ........................................ 90
Anhang ..................................................................... 91
Versicherung selbständiger Arbeit................99
"""

EXPECTED = """\
Qualitative Sozialforschung
Interpretation der Ergebnisse
Interpretation der Ergebnisse der Konsumtagebuecher anhand der quantitativen \
Auswertung durch statistische Daten
Interpretation der Ergebnisse der Frageboegen anhand der qualitativen Auswertung \
durch die qualitative Inhaltsanalyse nach Mayring
Beantwortung der Forschungsfragen und Hypothesen sowie Fazit und weiterführende Fragen
Literatur- und Quellenverzeichnis
Abbildungs- und Tabellenverzeichnis
Anhang
Versicherung selbständiger Arbeit"""


def test_toc_parse_content():
    parsed = gtsr.parse(CONTENT)
    assert len(parsed) == 9
    result = utilo.NEWLINE.join([item.title for item in parsed])
    assert result == EXPECTED


MULTILINE = """\
Abbildung 1: Korotkow-Geräusche bei der auskultatorischen Blutdruckmessung [Elt01] ..................................... 3
Abbildung 2: Manschettendruckverlauf und Oszillationen bei der oszillometrischen Blutdruckmessung [Elt01] . 4
Abbildung 3: Volumenkompensationsmethode nach Penaz [Elt01] ....................................................................... 4
Abbildung 4: Messverfahren nach R. Aaslid und AO. Brubakk [Aas81] ................................................................... 5
"""


def test_parse_page_multiline():
    parsed = gtsr.parse(MULTILINE)
    assert len(parsed) == 4
