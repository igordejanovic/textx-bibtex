"""
Remove comments from bib file.
"""
from bibparser import parse_bibtex, bibentry_str

BIB_FILE = '../references.bib'


bibfile = parse_bibtex(BIB_FILE)

# Drop line comments. They are artifacts from invalid file handling.
print('\n'.join([bibentry_str(e) for e in bibfile.entries
                 if e.__class__.__name__ != 'BibLineComment']))
