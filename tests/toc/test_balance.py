# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import reftable.toc.strategy.balance

RAW = """\
      Vorwort.............................................................................   5
1.  Einleitung
1.1  Zum Thema...........................................................................     9
1.2. Zum Untersuchungsgegenstand im engeren Sinne:  politisch-gesellschaftlichem System der DDR und Gesellschaft.................     12
1.3.  Der Aufbau der Arbeit ..........................................................     21
1.4.  Quellen, Literatur, Dokumente................................................     27
2. Der politische Kontext - Zu den Ursachen des Umbruchs   in der DDR ........................................     31
2.1.  Partei-Staat-Gesellschaft - Zur inneren Logik der    Reformunfähigkeit des DDR-Sozialismus
2.1.1.  Der ideologische Aspekt.............................................................     34
2.1.2.  Der ökonomische Aspekt ...........................................................     46
"""


def test_borders_best():
    lines = reftable.toc.strategy.balance.borders_best(RAW)
    assert len(lines) == 10
