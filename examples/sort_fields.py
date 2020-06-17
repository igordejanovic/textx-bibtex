"""
Sort fields in the bibtex entry by the given order.

Usage:
- Set BIB_FILE
- python sort_fields.py > new_references.bib
"""
from textx import metamodel_for_language
from txbibtex import bibfile_str


BIB_FILE = 'references.bib'

bibfile = metamodel_for_language('bibtex').model_from_file(BIB_FILE)

# Sort order
# Default order is 50
# fields with order lower than 50 will be at the beginning
# fields with order higher than 50 will be at the end
order = {
    'title': 1,
    'author': 2,
    'year': 3,
    'keywords': 100,
    'project': 101,
    'rank': 102
}

print(bibfile_str(bibfile, field_sort_order=order))
