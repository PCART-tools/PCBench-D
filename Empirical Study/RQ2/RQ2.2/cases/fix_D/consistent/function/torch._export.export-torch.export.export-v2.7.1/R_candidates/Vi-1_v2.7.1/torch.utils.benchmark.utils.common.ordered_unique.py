def ordered_unique(elements: Iterable[Any]) -> list[Any]:
    return list(collections.OrderedDict(dict.fromkeys(elements)).keys())
