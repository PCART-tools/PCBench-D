@substitute_in_graph(itertools.chain, is_embedded_type=True)  # type: ignore[arg-type]
def chain(*iterables: Iterable[_T]) -> Iterator[_T]:
    for iterable in iterables:
        yield from iterable
