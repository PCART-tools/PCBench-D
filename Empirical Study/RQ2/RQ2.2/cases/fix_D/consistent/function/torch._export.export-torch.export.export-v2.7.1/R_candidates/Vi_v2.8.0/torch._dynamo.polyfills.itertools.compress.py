@substitute_in_graph(itertools.compress, is_embedded_type=True)  # type: ignore[arg-type]
def compress(data: Iterable[_T], selectors: Iterable[_U], /) -> Iterator[_T]:
    return (datum for datum, selector in zip(data, selectors) if selector)
