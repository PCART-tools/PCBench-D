def _strlen_func():
    if compat.PY3:  # pragma: no cover
        _strlen = len
    else:
        encoding = get_option("display.encoding")

        def _strlen(x):
            try:
                return len(x.decode(encoding))
            except UnicodeError:
                return len(x)

    return _strlen
