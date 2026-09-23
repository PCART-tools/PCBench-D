@substitute_in_graph(itertools.dropwhile, is_embedded_type=True)  # type: ignore[arg-type]
def dropwhile(predicate: _Predicate[_T], iterable: Iterable[_T], /) -> Iterator[_T]:
    # dropwhile(lambda x: x < 5, [1, 4, 6, 3, 8]) -> 6 3 8

    iterator = iter(iterable)
    for x in iterator:
        if not predicate(x):
            yield x
            break

    yield from iterator
