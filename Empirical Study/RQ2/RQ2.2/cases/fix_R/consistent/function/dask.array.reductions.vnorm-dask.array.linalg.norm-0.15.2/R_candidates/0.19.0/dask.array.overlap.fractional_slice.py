def fractional_slice(task, axes):
    """

    >>> fractional_slice(('x', 5.1), {0: 2})  # doctest: +SKIP
    (getitem, ('x', 6), (slice(0, 2),))

    >>> fractional_slice(('x', 3, 5.1), {0: 2, 1: 3})  # doctest: +SKIP
    (getitem, ('x', 3, 5), (slice(None, None, None), slice(-3, None)))

    >>> fractional_slice(('x', 2.9, 5.1), {0: 2, 1: 3})  # doctest: +SKIP
    (getitem, ('x', 3, 5), (slice(0, 2), slice(-3, None)))
    """
    rounded = (task[0],) + tuple(int(round(i)) for i in task[1:])

    index = []
    for i, (t, r) in enumerate(zip(task[1:], rounded[1:])):
        depth = axes.get(i, 0)
        if t == r:
            index.append(slice(None, None, None))
        elif t < r:
            index.append(slice(0, depth))
        elif t > r and depth == 0:
            index.append(slice(0, 0))
        else:
            index.append(slice(-depth, None))

    index = tuple(index)

    if all(ind == slice(None, None, None) for ind in index):
        return task
    else:
        return (getitem, rounded, index)
