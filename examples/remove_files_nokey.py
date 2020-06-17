"""
Remove files with no corresponding key in the bib file
"""
import os
from bibparser import parse_bibtex

BIB_FILE = '../references.bib'
DOCS_FOLDER = '../docs/'


bibfile = parse_bibtex(BIB_FILE)
bibkeys = [e.key for e in bibfile.entries
           if e.__class__.__name__ == 'BibRefEntry']

bibkeys = set(bibkeys)
file_names = []
for f in os.listdir(DOCS_FOLDER):
    file_name = os.path.splitext(os.path.basename(f))[0]
    if file_name not in bibkeys:
        print(f'rm \'{DOCS_FOLDER}{f}\'')
