@substitute_in_graph(itertools.chain.from_iterable)  # type: ignore[arg-type]
def chain_from_iterable(iterable: Iterable[Iterable[_T]], /) -> Iterator[_T]:
    return itertools.chain(*iterable)
