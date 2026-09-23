def unique(it: Iterable[_T]) -> ValuesView[_T]:
    return {id(x): x for x in it}.values()
