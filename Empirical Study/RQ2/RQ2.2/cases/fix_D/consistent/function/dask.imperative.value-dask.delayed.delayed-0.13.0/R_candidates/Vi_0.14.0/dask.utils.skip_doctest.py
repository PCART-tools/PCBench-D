def skip_doctest(doc):
    if doc is None:
        return ''
    return '\n'.join([_skip_doctest(line) for line in doc.split('\n')])
