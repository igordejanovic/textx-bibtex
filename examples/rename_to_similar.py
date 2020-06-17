"""
Rename files from docs folder with missing bib key to the bib key that is most
similar.
"""
import os
from difflib import SequenceMatcher

from bibparser import parse_bibtex

BIB_FILE = '../references.bib'
DOCS_FOLDER = '../docs/'

bibfile = parse_bibtex(BIB_FILE)

bibkeys = [e.key for e in bibfile.entries
           if e.__class__.__name__ == 'BibRefEntry']


bibkeys = set(bibkeys)
missing_file = []
file_names = []
for f in os.listdir(DOCS_FOLDER):
    file_name = os.path.splitext(os.path.basename(f))[0]
    file_names.append(file_name)
    if file_name not in bibkeys:
        missing_file.append(f)

# Get only keys that don't have corresponding file
bibkeys = [key for key in bibkeys if key not in file_names]

print('# Missing keys: ', len(missing_file))
print('# Missing file: ', len(bibkeys))

# For all missing keys find most similar
missing_similar = []
for m in missing_file:
    m_key, m_ext = os.path.splitext(m)
    m_key_similar = sorted(bibkeys,
                           key=lambda key: SequenceMatcher(
                               None, m_key, key).ratio(),
                           reverse=True)[0]
    print(f'mv \'{DOCS_FOLDER}{m_key}{m_ext}\' {DOCS_FOLDER}{m_key_similar}{m_ext}')  # noqa
