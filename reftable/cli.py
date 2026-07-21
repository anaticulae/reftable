#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utilo

import reftable

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'abbrev',
        inputs=[
            utilo.ResultFile(producer='rawmaker', name='text_text'),
            utilo.ResultFile(producer='rawmaker', name='text_positions'),
            utilo.ResultFile(producer='rawmaker', name='oneline_text_text'),
            utilo.ResultFile('rawmaker', name='oneline_text_positions'),
            utilo.ResultFile(producer='groupme', name='footer_footerheader'),
            utilo.ResultFile(producer='rawmaker', name='border_pages'),
        ],
        output=('abbrev',),
    ),
    utilo.create_step(
        'toc',
        inputs=[
            utilo.ResultFile(producer='rawmaker', name='oneline_text_text'),
            utilo.ResultFile('rawmaker', name='oneline_text_positions'),
            utilo.ResultFile(producer='groupme', name='footer_footerheader'),
            utilo.ResultFile(producer='rawmaker', name='border_pages'),
        ],
        output=('toc',),
    ),
    utilo.create_step(
        'figure',
        inputs=[
            utilo.ResultFile(producer='rawmaker', name='text_text'),
            utilo.ResultFile(producer='rawmaker', name='text_positions'),
            utilo.ResultFile(producer='rawmaker', name='oneline_text_text'),
            utilo.ResultFile('rawmaker', name='oneline_text_positions'),
            utilo.ResultFile(producer='groupme', name='footer_footerheader'),
            utilo.ResultFile(producer='rawmaker', name='border_pages'),
        ],
        output=('figure',),
    ),
    utilo.create_step(
        'table',
        inputs=[
            utilo.ResultFile(producer='rawmaker', name='oneline_text_text'),
            utilo.ResultFile('rawmaker', name='oneline_text_positions'),
            utilo.ResultFile(producer='groupme', name='footer_footerheader'),
            utilo.ResultFile(producer='rawmaker', name='border_pages'),
        ],
        output=('table',),
    ),
]


def main():
    utilo.featurepack(
        workplan=WORKPLAN,
        root=reftable.ROOT,
        featurepackage='reftable.feature',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=reftable.PROCESS,
            pages=True,
            version=reftable.__version__,
        ),
    )
