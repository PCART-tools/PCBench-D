def _skip_doctest(line):
    if '>>>' in line:
        return line + '    # doctest: +SKIP'
    else:
        return line
