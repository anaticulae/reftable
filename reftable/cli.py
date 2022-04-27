#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila

import reftable

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'abbrev',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='text_text'),
            utila.ResultFile(producer='rawmaker', name='text_positions'),
            utila.ResultFile(producer='rawmaker', name='oneline_text_text'),
            utila.ResultFile('rawmaker', name='oneline_text_positions'),
        ],
        output=('abbrev',),
    ),
    utila.create_step(
        'toc',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='oneline_text_text'),
            utila.ResultFile('rawmaker', name='oneline_text_positions'),
            utila.ResultFile(producer='groupme', name='footer_footerheader'),
            utila.ResultFile(producer='rawmaker', name='border_pages'),
        ],
        output=('toc',),
    ),
    utila.create_step(
        'figure',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='text_text'),
            utila.ResultFile(producer='rawmaker', name='text_positions'),
            utila.ResultFile(producer='rawmaker', name='oneline_text_text'),
            utila.ResultFile('rawmaker', name='oneline_text_positions'),
            utila.ResultFile(producer='groupme', name='footer_footerheader'),
            utila.ResultFile(producer='rawmaker', name='border_pages'),
        ],
        output=('figure',),
    ),
    utila.create_step(
        'table',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='oneline_text_text'),
            utila.ResultFile('rawmaker', name='oneline_text_positions'),
            utila.ResultFile(producer='groupme', name='footer_footerheader'),
            utila.ResultFile(producer='rawmaker', name='border_pages'),
        ],
        output=('table',),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=reftable.ROOT,
        featurepackage='reftable.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=reftable.PROCESS,
            pages=True,
            version=reftable.__version__,
        ),
    )
