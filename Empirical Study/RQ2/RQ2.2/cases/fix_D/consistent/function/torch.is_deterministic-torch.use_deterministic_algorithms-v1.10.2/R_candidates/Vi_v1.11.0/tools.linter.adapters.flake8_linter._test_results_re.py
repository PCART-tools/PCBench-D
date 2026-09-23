def _test_results_re() -> None:
    """
    >>> def t(s): return RESULTS_RE.search(s).groupdict()

    >>> t(r"file.py:80:1: E302 expected 2 blank lines, found 1")
    ... # doctest: +NORMALIZE_WHITESPACE
    {'file': 'file.py', 'line': '80', 'column': '1', 'code': 'E302',
     'message': 'expected 2 blank lines, found 1'}

    >>> t(r"file.py:7:1: P201: Resource `stdout` is acquired but not always released.")
    ... # doctest: +NORMALIZE_WHITESPACE
    {'file': 'file.py', 'line': '7', 'column': '1', 'code': 'P201',
     'message': 'Resource `stdout` is acquired but not always released.'}

    >>> t(r"file.py:8:-10: W605 invalid escape sequence '/'")
    ... # doctest: +NORMALIZE_WHITESPACE
    {'file': 'file.py', 'line': '8', 'column': '-10', 'code': 'W605',
     'message': "invalid escape sequence '/'"}
    """
    pass
