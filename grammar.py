#!/bin/python3
# -*- coding: utf-8 -*-
"""
this module provide methods used for processing grammar

related works.
"""

is_zh = (lambda x: True if 19968 <= ord(x) <= 40908 else False)

grammar_type = {'S': ['N'],
                'P': ['V','A'],
                'O': ['N']}
