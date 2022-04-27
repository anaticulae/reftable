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
    (power.HC_DISS193, '9:13'),
    (power.DISS172_PDF, '0:10'),
    (power.HC_DISS171, '0:10'),
    (power.HC_DISS166, '0:10'),
    (power.MASTER155_PDF, '0:10'),
    (power.HC_DISS148, '0:10'),
    (power.DISS143_PDF, '0:12'),
    (power.BACHELOR128_PDF, '0:10'),
    (power.HC_DISS128, '0:10'),
    (power.MASTER127_PDF, '0:11'),
    (power.BACHELOR111_PDF, '0:10,90:111'),
    (power.BACHELOR105_PDF, '0:5'),
    (power.BACHELOR101_PDF, '0:5'),
    (power.MASTER110_PDF, '0:10'),
    (power.BACHELOR241_PDF, '0:100'),
    (power.DISS480_PDF, '0:10'),
    (power.BOOK173_PDF, '0:100'),
    (power.MASTER089_PDF, '0:10,75:89'),
    (power.BACHELOR086_PDF, '0:10'),
    (power.BACHELOR078_PDF, '0:10'),
    (power.MASTER075_PDF, '70:75'),
    (power.MASTER072_PDF, '0:10'),
    (power.DISS406_PDF, '0:75,100:150'),
    (power.BACHELOR037_PDF, '0:10'),
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
    (power.MASTER049_PDF, '0:10'),
    (power.BACHELOR041A_PDF, '0:10'),
    (power.BACHELOR039_PDF, '0:10'),
    (power.BACHELOR032_PDF, '0:10'),
    (power.BACHELOR032A_PDF, '0:10'),
    (power.BACHELOR028_PDF, '0:10'),
    (power.DOCU027_PDF, '0:5'),
    (power.TECH024_PDF, '0:5'),
    (power.HOME050_PDF, '0:10'),
    (power.MASTER083_PDF, '0:10'),
    (power.DOCU035_PDF, '0:10'),
    (power.DISS180_PDF, '0:10'),
    (power.MASTER078_PDF, '0:10'),
    (power.DISS157_PDF, '6:10'),
    (power.MASTER099B_PDF, '2'),
    (power.MASTER193_PDF, '3,4,5'),
    (power.MASTER112_PDF, '5,6'),
    (power.MASTER116_PDF, '96'),
    (power.DISS205_PDF, '14'),
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
