def _assert2d(*arrays):
    for a in arrays:
        if a.ndim != 2:
            raise ValueError(f'{a.ndim}-dimensional array given. '
                             'Array must be two-dimensional')
