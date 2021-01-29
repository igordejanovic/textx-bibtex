#!/usr/bin/env python3
#
# Given the input bibtex file and the orgmode file using org-ref create bibtex
# file with only references used eliminating duplicates.

import sys
from textx import metamodel_for_language, metamodel_from_str
from txbibtex import bibentry_str

if len(sys.argv) != 4:
    print('Usage: extract_org_ref_cites.py mypaper.org references.bib output.bib')
    print('Last parameter is the name of the output that gets overwriten!')
    exit(1)

ORGFILE, BIB_IN, BIB_OUT = sys.argv[1:]

cite_grammar = r'''
Cites: (/(?!cite)./ | cites+=Cite | 'cite' )*;
Cite: 'cite:' refs+=ID[','];
'''

# Get the textX model from the bib file
bib_in = metamodel_for_language('bibtex').model_from_file(BIB_IN)
orgfile = metamodel_from_str(cite_grammar).model_from_file(ORGFILE)

# Get all keys from orgmode file without dupes
keys = {ref for cite in orgfile.cites for ref in cite.refs}

# Get all entries in references database
bibentries = {e.key: e for e in bib_in.entries if e.__class__.__name__ == 'BibRefEntry'}

with open(BIB_OUT, 'w') as f:
    for key in keys:
        if key not in bibentries:
            print('Key "{}" not found in reference database.'.format(key))
        else:
            f.write(bibentry_str(bibentries[key]))
