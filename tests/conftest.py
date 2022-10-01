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
import utilatest
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

import reftable

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = reftable.PROCESS

RESOURCES = [
    (power.BACHELOR028_PDF, '0:10'),
    (power.BACHELOR032A_PDF, '0:10'),
    (power.BACHELOR032_PDF, '0:10'),
    (power.BACHELOR037_PDF, '0:10'),
    (power.BACHELOR039_PDF, '0:10'),
    (power.BACHELOR041A_PDF, '0:10'),
    (power.BACHELOR063_PDF, '0:9,59:62'),
    (power.BACHELOR076_PDF, '0:25'),
    (power.BACHELOR078_PDF, '0:10'),
    (power.BACHELOR086_PDF, '0:10'),
    (power.BACHELOR090_PDF, '0:25'),
    (power.BACHELOR101_PDF, '0:5'),
    (power.BACHELOR105_PDF, '0:5'),
    (power.BACHELOR111_PDF, '0:10,90:111'),
    (power.BACHELOR128_PDF, '0:10'),
    (power.BACHELOR241_PDF, '0:100'),
    (power.BOOK173_PDF, '0:100'),
    (power.DISS143_PDF, '0:12'),
    (power.DISS157_PDF, '6:10'),
    (power.DISS172_PDF, '0:10'),
    (power.DISS178_PDF, '0:30'),
    (power.DISS180_PDF, '0:10'),
    (power.DISS205_PDF, '14'),
    (power.DISS406_PDF, '0:75,100:150'),
    (power.DISS480_PDF, '0:10'),
    (power.DOCU027_PDF, '0:5'),
    (power.DOCU035_PDF, '0:10'),
    (power.HC_DISS128, '0:10'),
    (power.HC_DISS148, '0:10'),
    (power.HC_DISS166, '0:10'),
    (power.HC_DISS171, '0:10'),
    (power.HC_DISS193, '9:13'),
    (power.HOME007_PDF, ':'),
    (power.HOME012_PDF, '1'),
    (power.HOME014_PDF, '1'),
    (power.HOME014B_PDF, '1'),
    (power.HOME014C_PDF, '1'),
    (power.HOME015_PDF, '1'),
    (power.HOME016_PDF, '1'),
    (power.HOME017C_PDF, '0:10'),
    (power.HOME018_PDF, '2'),
    (power.HOME019_PDF, '0:10'),
    (power.HOME019A_PDF, '1'),
    (power.HOME019B_PDF, '0:10'),
    (power.HOME020_PDF, '1'),
    (power.HOME021_PDF, '0,1'),
    (power.HOME021A_PDF, '1'),
    (power.HOME021B_PDF, '0:10'),
    (power.HOME022_PDF, '0:10'),
    (power.HOME022A_PDF, '1'),
    (power.HOME050_PDF, '0:10'),
    (power.MASTER049_PDF, '0:10'),
    (power.MASTER072_PDF, '0:10'),
    (power.MASTER075_PDF, '70:75'),
    (power.MASTER078_PDF, '0:10'),
    (power.MASTER083_PDF, '0:10'),
    (power.MASTER089_PDF, '0:10,75:89'),
    (power.MASTER098_PDF, '0:15'),
    (power.MASTER099B_PDF, '2'),
    (power.MASTER099_PDF, '0:30'),
    (power.MASTER110_PDF, '0:10'),
    (power.MASTER112_PDF, '5,6'),
    (power.MASTER116_PDF, '96'),
    (power.MASTER127_PDF, '0:11'),
    (power.MASTER155_PDF, '0:10'),
    (power.MASTER193_PDF, '3,4,5'),
    (power.PAPER14B_PDF, '1'),
    (power.TECH024_PDF, '0:5'),
    power.TECH019_PDF,
    genex.todo(
        power.DOCU007_PDF,
        groupme='--content',
        cleanup=True,
        footnote=True,
        headnote=True,
        pagenumber=True,
        tablero=True,
    ),
]

WORKER = utilatest.worker_count(6, onci=len(RESOURCES))


def pytest_sessionstart(session):  # pylint:disable=W0613
    power.run()


def extract(resources):
    genex.extract(
        resources,
        cleanup=True,
        pagenumber=True,
        footnote=True,
        sections=True,
        worker=WORKER,
    )
