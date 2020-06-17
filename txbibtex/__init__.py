# -*- coding: utf-8 -*-
#######################################################################
# Name: bibtex.py
# Purpose: Parser for bibtex files
# Author: Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2020 Igor R. Dejanovic
#    <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
#######################################################################
import os
from functools import partial
from textx import language, metamodel_from_file

__version__ = "0.1.0.dev"


@language('bibtex', '*.bib')
def bibtex_language():
    "The BibTeX language"
    current_dir = os.path.dirname(__file__)
    mm = metamodel_from_file(os.path.join(current_dir, 'bibtex.tx'))

    def strip_value(v):
        if (v.startswith('{') and v.endswith('}')) or \
          (v.startswith('"') and v.endswith('"')):
            return v[1:-1]
        return v

    mm.register_obj_processors({
        'Value': strip_value
    })

    return mm


def bibfile_str(self, bibfile, field_sort_order=None):
    return '\n'.join([bibentry_str(v, field_sort_order)
                      for v in bibfile.entries])


def bibentry_str(bibentry, field_sort_order={}):
    if bibentry.__class__.__name__ == 'BibLineComment':
        s = bibentry.text
    elif bibentry.__class__.__name__ == 'BibComment':
        s = f'@comment{{{bibentry.text}}}'
    elif bibentry.__class__.__name__ == 'BibPreamble':
        s = f'@preamble{{\n    {bibentry.value}\n}}'
    else:
        s = f"@{bibentry.type}{{{bibentry.key},\n    "
        s += ',\n    '.join(
            [bibfield_str(f)
             for f in sorted(bibentry.fields,
                             key=partial(field_sort_key,
                                         field_sort_order=field_sort_order))])
        s += '\n}\n'
    return s


def field_sort_key(field, field_sort_order):
    return field_sort_order.get(field.name, 50) if field_sort_order else 50


def bibfield_str(b):
    return f'{b.name} = {{{b.value}}}'
