# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import elements

# minimal percentage of figure lines per page
TOFS_PER_PAGE_MIN = configo.HV_PERCENT_PLUS(default=20, limit=100.0)

NO_FIGURES = (elements.ABBREVIATION | elements.BIBLIOGRAPHY |
              elements.GLOSSARY | elements.SYMBOLTABLE | elements.TABLETABLE |
              elements.TOC)
