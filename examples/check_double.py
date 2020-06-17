"""
Check bib file for double keys.
"""
from collections import Counter
from textx import metamodel_for_language

BIB_FILE = 'references.bib'

# Get the textX model from the bib file
bibfile = metamodel_for_language('bibtex').model_from_file(BIB_FILE)

bibkeys = [e.key for e in bibfile.entries
           if e.__class__.__name__ == 'BibRefEntry']

# Check double keys
counts = Counter(bibkeys)
print(counts.most_common(5))

assert len(bibkeys) == len(set(bibkeys))
