def _length_check(others):
    n = None
    for x in others:
        try:
            if n is None:
                n = len(x)
            elif len(x) != n:
                raise ValueError('All arrays must be same length')
        except TypeError:
            raise ValueError("Did you mean to supply a `sep` keyword?")
    return n
