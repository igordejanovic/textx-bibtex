"""
Remove comments from bib file.
"""
from textx import metamodel_for_language
from txbibtex import bibentry_str

BIB_FILE = 'references.bib'
bibfile = metamodel_for_language('bibtex').model_from_file(BIB_FILE)

# Drop line comments.
print('\n'.join([bibentry_str(e) for e in bibfile.entries
                 if e.__class__.__name__ != 'BibLineComment']))
