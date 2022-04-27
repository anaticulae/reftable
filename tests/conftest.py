# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power

import reftable

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = reftable.PROCESS

RESOURCES = [
    power.HC_DISS193,
    power.DISS172_PDF,
    power.HC_DISS171,
    power.HC_DISS166,
    power.MASTER155_PDF,
    power.HC_DISS148,
    power.DISS143_PDF,
    power.BACHELOR128_PDF,
    power.HC_DISS128,
    power.MASTER127_PDF,
    power.BACHELOR111_PDF,
    power.BACHELOR105_PDF,
    power.BACHELOR101_PDF,
    power.MASTER110_PDF,
    (power.BACHELOR241_PDF, '0:100'),
    power.DISS480_PDF,
    (power.BOOK173_PDF, '0:100'),
    power.MASTER089_PDF,
    power.BACHELOR086_PDF,
    power.BACHELOR078_PDF,
    power.MASTER075_PDF,
    power.MASTER072_PDF,
    (power.DISS406_PDF, '0:75,100:150'),
    power.BACHELOR037_PDF,
    (power.MASTER099_PDF, '0:30'),
    (power.MASTER098_PDF, '0:15'),
    (power.BACHELOR090_PDF, '0:25'),
    (power.BACHELOR076_PDF, '0:25'),
    (power.BACHELOR063_PDF, '0:9,59:62'),
    (power.DISS178_PDF, '0:30'),
    genex.todo(
        power.DOCU007_PDF,
        groupme='--pagenumbers --footer --content',
        tablero=True,
    ),
    power.MASTER049_PDF,
    power.BACHELOR041A_PDF,
    power.BACHELOR039_PDF,
    power.BACHELOR032_PDF,
    power.BACHELOR032A_PDF,
    power.BACHELOR028_PDF,
    power.DOCU027_PDF,
    power.TECH024_PDF,
    (power.HOME050_PDF, '0:10'),
    (power.MASTER083_PDF, '0:10'),
    (power.DOCU035_PDF, '0:10'),
    (power.DISS180_PDF, '0:10'),
    (power.MASTER078_PDF, '0:10'),
    (power.DISS157_PDF, '6:10'),
    (power.MASTER099B_PDF, '2'),
    (power.MASTER193_PDF, '3,4,5'),
    (power.MASTER112_PDF, '5,6'),
]

WORKER = 5


def pytest_sessionstart(session):  # pylint:disable=W0613
    power.run()


def extract(resources):
    destination = power.generated()
    genex.extract(
        resources,
        destination=destination,
        groupme='--pagenumbers --footer',
        worker=WORKER,
        pages=':',
        base=power.REPOSITORY,
    )
