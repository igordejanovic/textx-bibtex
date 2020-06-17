"""
Normalize all bib keys to <author><year> and rename pdf files along the way.
"""
import os
import unidecode
import re
from textx import metamodel_for_language
from txbibtex import bibfile_str

BIB_FILE = '../references.bib'
DOCS_FOLDER = '../docs/'


nonkeychars = re.compile('[^a-zA-Z0-9]')

bibfile = metamodel_for_language('bibtex').model_from_file(BIB_FILE)
bibkeys = set([e.key for e in bibfile.entries
               if e.__class__.__name__ == 'BibRefEntry'])


def to_key(k):
    k = unidecode.unidecode(k.strip().lower())
    k = nonkeychars.sub('', k)
    return k


def resolve_key(old_key, k):
    newk = k
    i = ord('a')
    while newk in bibkeys:
        # Resolve collision by adding a, b, c,...
        letter = chr(i)
        newk = k + letter
        i += 1
    bibkeys.remove(old_key)
    bibkeys.add(newk)
    return newk


def get_author(f):
    astr = f.value
    if ' and ' in astr:
        astr = astr.split(' and ')[0]
    if ',' in astr:
        astr = astr.split(',')[0]
        astr = astr.replace(' ', '')
    return to_key(astr.split()[0])


def get_field(e, name):
    fields = [f for f in e.fields if f.name == name]
    if fields:
        return fields[0]


# Get filenames and extensions
file_names = {}
for f in os.listdir(DOCS_FOLDER):
    file_name, ext = os.path.splitext(os.path.basename(f))
    file_names[file_name] = ext

mv_file = ''
for e in bibfile.entries:
    if e.__class__.__name__ == 'BibRefEntry':
        author_field = get_field(e, 'author')
        year_field = get_field(e, 'year')
        title_field = get_field(e, 'title')
        new_key = None
        if author_field and year_field:
            new_key = "{}{}".format(get_author(author_field),
                                    to_key(year_field.value))
        elif title_field and year_field:
            new_key = "{}{}".format(to_key(title_field.value[:10]),
                                    to_key(year_field.value))
        else:
            new_key = to_key(e.key)

        if new_key and new_key != e.key:
            new_key = resolve_key(e.key, new_key)
            if e.key in file_names:
                ext = file_names[e.key]
                if "'" in e.key:
                    mv_file += f'mv "{DOCS_FOLDER}{e.key}{ext}" {DOCS_FOLDER}{new_key}{ext}\n'  # noqa
                else:
                    mv_file += f"mv '{DOCS_FOLDER}{e.key}{ext}' {DOCS_FOLDER}{new_key}{ext}\n"  # noqa
        else:
            print('Not changed: ', e.key)

        e.key = new_key


# Write new reference file and script for file renames
print('Writing rename_docs.sh')
with open('rename_docs.sh', 'w') as f:
    f.write(mv_file)

print('Writing references-fixed.sh')
with open('references-fixed.bib', 'w') as f:
    f.write(bibfile_str(bibfile))

print('Investigate results and apply.')
