#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 07:22:54 2023

@author: bjorn
"""

# default = {"Biopython_version": bpversion,
#           "func": f"{Tm_NN.__module__}.{Tm_NN.__name__}"}
# {'seq',
#  'check',
#  'strict',
#  'c_seq',
#  'shift',
#  'nn_table': 4,
#  'tmm_table',
#  'imm_table',
#  'de_table',
#  'dnac1': 250,
#  'dnac2': 250,
#  'selfcomp',
#  'Na': 40,
#  'K': 0,,
#  'Tris': 75.0,
#  'Mg': 1.5,
#  'dNTPs': 0.8,
#  'saltcorr': 7}


# {'seq',
#  'check',
#  'strict',
#  'c_seq',
#  'shift',
#  'nn_table': 4,
#  'tmm_table',
#  'imm_table',
#  'de_table',
#  'dnac1': 250,
#  'dnac2': 250,
#  'selfcomp',
#  'Na': 40,
#  'K': 0,,
#  'Tris': 75.0,
#  'Mg': 1.5,
#  'dNTPs': 0.8,
#  'saltcorr': 7}


# from Bio.SeqUtils.MeltingTemp import Tm_NN, DNA_NN4
#
# f"""
# Tm_NN("ATGGCAGTTGAGAAGA",
#       check=True,
#       strict=True,
#       c_seq=None,
#       shift=0,
#       nn_table={nn_table},
#       tmm_table=None,
#       imm_table=None,
#       de_table=None,
#       dnac1={dnac1},
#       dnac2={dnac2},
#       selfcomp=False,
#       Na={Na},
#       K={K},
#       Tris={},
#       Mg={Mg},
#       dNTPs={dNTPs},
#       saltcorr={saltcorr},):
# """
#
#
# {'seq',
# 'check',
# 'strict',
# 'c_seq',
# 'shift',
# 'nn_table': 4,
# 'tmm_table',
# 'imm_table',
# 'de_table',
# 'dnac1': 250,
# 'dnac2': 250,
# 'selfcomp',
# 'Na': 40,
# 'K': 0,
# 'Tris': 75.0,
# 'Mg': 1.5,
# 'dNTPs': 0.8,
# 'saltcorr': 7}
#
#
# from pydna.tm import tm_default
#
# import inspect
#
# sign = inspect.signature(tm_default)
#
# list(sign.parameters.keys())
#
