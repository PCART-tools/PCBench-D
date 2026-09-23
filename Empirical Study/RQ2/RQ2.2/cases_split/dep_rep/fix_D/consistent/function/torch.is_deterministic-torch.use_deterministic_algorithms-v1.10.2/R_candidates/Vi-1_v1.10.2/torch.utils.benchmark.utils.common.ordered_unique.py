def ordered_unique(elements: Iterable[Any]) -> List[Any]:
    return list(collections.OrderedDict({i: None for i in elements}).keys())
