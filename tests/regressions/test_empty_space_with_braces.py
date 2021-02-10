from textx import metamodel_for_language


grammar = r'''
@incollection{visser2008,
    title = {{W}eb{DSL}: {A} {C}ase {S}tudy in {D}omain-{S}pecific {L}anguage {E}ngineering},
    author = {Visser, Eelco},
    year = {2008},
    booktitle = {Generative and Transformational Techniques in Software Engineering II},
    doi = {10.1007/978-3-540-88643-3_7},
    editor = {Lämmel, Ralf and Visser, Joost and Saraiva, João},
    isbn = {978-3-540-88642-6},
    pages = {291–373},
    publisher = {Springer Berlin Heidelberg},
    series = {Lecture Notes in Computer Science},
    url = {http://dx.doi.org/10.1007/978-3-540-88643-3_7},
    volume = {5235},
    keywords = {dslbook}
}
'''


def test_space_with_braces():
    """
    Test a bug where spaces between } and { inside a value would be lost.
    """

    mm = metamodel_for_language('bibtex')
    model = mm.model_from_str(grammar)

    entry = model.entries[0]

    # Find title
    title = [f for f in entry.fields if f.name == 'title'][0].value

    # Check title, "{A} {Case}" should have a space in between
    assert title == '{W}eb{DSL}: {A} {C}ase {S}tudy in {D}omain-{S}pecific {L}anguage {E}ngineering'
