def _cluster(iterable: Iterable[Any], n: int = 2) -> Iterable[Any]:
    return zip(*[iter(iterable)] * n)
