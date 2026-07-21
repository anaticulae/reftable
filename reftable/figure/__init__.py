# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import elementae
import utilo

# minimal percentage of figure lines per page
TOFS_PER_PAGE_MIN = configos.HV_PERCENT_PLUS(default=20, limit=100.0)

NO_FIGURES = utilo.unique(elementae.ABBREVIATION + elementae.BIBLIOGRAPHY +
                          elementae.GLOSSARY + elementae.SYMBOLTABLE +
                          elementae.TABLETABLE + elementae.TOC)
