def _skip_doctest(line):
    # NumPy docstring contains cursor and comment only example
    stripped = line.strip()
    if stripped == '>>>' or stripped.startswith('>>> #'):
        return stripped
    elif '>>>' in stripped:
        return line + '    # doctest: +SKIP'
    else:
        return line
