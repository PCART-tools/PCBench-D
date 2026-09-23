    @substitute_in_graph(itertools.pairwise, is_embedded_type=True)  # type: ignore[arg-type]
    def pairwise(iterable: Iterable[_T], /) -> Iterator[tuple[_T, _T]]:
        a = None
        first = True
        for b in iterable:
            if first:
                first = False
            else:
                yield a, b  # type: ignore[misc]
            a = b
