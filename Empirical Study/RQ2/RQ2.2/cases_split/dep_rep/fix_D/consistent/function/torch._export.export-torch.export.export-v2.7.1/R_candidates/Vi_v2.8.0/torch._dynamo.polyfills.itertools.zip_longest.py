@substitute_in_graph(itertools.zip_longest, is_embedded_type=True)  # type: ignore[arg-type,misc]
def zip_longest(
    *iterables: Iterable[_T],
    fillvalue: _U = None,  # type: ignore[assignment]
) -> Iterator[tuple[_T | _U, ...]]:
    # zip_longest('ABCD', 'xy', fillvalue='-') -> Ax By C- D-

    iterators = list(map(iter, iterables))
    num_active = len(iterators)
    if not num_active:
        return

    while True:
        values = []
        for i, iterator in enumerate(iterators):
            try:
                value = next(iterator)
            except StopIteration:
                num_active -= 1
                if not num_active:
                    return
                iterators[i] = itertools.repeat(fillvalue)  # type: ignore[arg-type]
                value = fillvalue  # type: ignore[assignment]
            values.append(value)
        yield tuple(values)
