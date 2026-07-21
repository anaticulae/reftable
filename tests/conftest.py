# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import resinf
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import reftable

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = reftable.PROCESS

RESOURCES = [
    (hoverpower.BACHELOR028_PDF, '0:10'),
    (hoverpower.BACHELOR032A_PDF, '0:10'),
    (hoverpower.BACHELOR032_PDF, '0:10'),
    (hoverpower.BACHELOR037_PDF, '0:10'),
    (hoverpower.BACHELOR039_PDF, '0:10'),
    (hoverpower.BACHELOR041A_PDF, '0:10'),
    (hoverpower.BACHELOR063_PDF, '0:9,59:62'),
    (hoverpower.BACHELOR076_PDF, '0:25'),
    (hoverpower.BACHELOR078_PDF, '0:10'),
    (hoverpower.BACHELOR086_PDF, '0:10'),
    (hoverpower.BACHELOR090_PDF, '0:25'),
    (hoverpower.BACHELOR101_PDF, '0:5'),
    (hoverpower.BACHELOR105_PDF, '0:5'),
    (hoverpower.BACHELOR111_PDF, '0:10,90:111'),
    (hoverpower.BACHELOR128_PDF, '0:10'),
    (hoverpower.BACHELOR241_PDF, '0:100'),
    (hoverpower.BOOK173_PDF, '0:100'),
    (hoverpower.DISS143_PDF, '0:12'),
    (hoverpower.DISS154_PDF, '4:8'),
    (hoverpower.DISS157_PDF, '6:10'),
    (hoverpower.DISS172_PDF, '0:10'),
    (hoverpower.DISS178_PDF, '0:30'),
    (hoverpower.DISS180_PDF, '0:10'),
    (hoverpower.DISS205_PDF, '14'),
    (hoverpower.DISS406_PDF, '0:75,100:150'),
    (hoverpower.DISS480_PDF, '0:10'),
    (hoverpower.DOCU027_PDF, '0:5'),
    (hoverpower.DOCU035_PDF, '0:10'),
    (hoverpower.HC_DISS128, '0:10'),
    (hoverpower.HC_DISS148, '0:10'),
    (hoverpower.HC_DISS166, '0:10'),
    (hoverpower.HC_DISS171, '0:10'),
    (hoverpower.HC_DISS193, '9:13'),
    (hoverpower.HOME007_PDF, ':'),
    (hoverpower.HOME012_PDF, '1'),
    (hoverpower.HOME014_PDF, '1'),
    (hoverpower.HOME014B_PDF, '1'),
    (hoverpower.HOME014C_PDF, '1'),
    (hoverpower.HOME015_PDF, '1'),
    (hoverpower.HOME016_PDF, '1'),
    (hoverpower.HOME017C_PDF, '0:10'),
    (hoverpower.HOME018_PDF, '2'),
    (hoverpower.HOME019_PDF, '0:10'),
    (hoverpower.HOME019A_PDF, '1'),
    (hoverpower.HOME019B_PDF, '0:10'),
    (hoverpower.HOME020_PDF, '1'),
    (hoverpower.HOME021_PDF, '0,1'),
    (hoverpower.HOME021A_PDF, '1'),
    (hoverpower.HOME021B_PDF, '0:10'),
    (hoverpower.HOME022_PDF, '0:10'),
    (hoverpower.HOME022A_PDF, '1'),
    (hoverpower.HOME050_PDF, '0:10'),
    (hoverpower.MASTER049_PDF, '0:10'),
    (hoverpower.MASTER072_PDF, '0:10'),
    (hoverpower.MASTER075_PDF, '70:75'),
    (hoverpower.MASTER078_PDF, '0:10'),
    (hoverpower.MASTER083_PDF, '0:10'),
    (hoverpower.MASTER089_PDF, '0:10,75:89'),
    (hoverpower.MASTER098_PDF, '0:15'),
    (hoverpower.MASTER099B_PDF, '2'),
    (hoverpower.MASTER099_PDF, '0:30'),
    (hoverpower.MASTER110_PDF, '0:10'),
    (hoverpower.MASTER112_PDF, '5,6'),
    (hoverpower.MASTER116_PDF, '96'),
    (hoverpower.MASTER127_PDF, '0:11'),
    (hoverpower.MASTER155_PDF, '0:10'),
    (hoverpower.MASTER193_PDF, '3,4,5'),
    (hoverpower.PAPER14B_PDF, '1'),
    (hoverpower.TECH024_PDF, '0:5'),
    hoverpower.TECH019_PDF,
    resinf.todo(
        hoverpower.DOCU007_PDF,
        cleanup=True,
        footnote=True,
        groupme='--content --hefopa',
        headnote=True,
        pagenumber=True,
        tablero=True,
    ),
]

WORKER = utilotest.worker_count(6, onci=len(RESOURCES))


def pytest_sessionstart(session):  # pylint:disable=W0613
    hoverpower.run()


def extract(resources):
    gennex.extract(
        resources,
        cleanup=True,
        footnote=True,
        groupme='--content --hefopa',
        headnote=True,
        pagenumber=True,
        sections=True,
        worker=WORKER,
    )
