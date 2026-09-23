def ordered_set(*items: T) -> dict[T, Literal[True]]:
    return dict.fromkeys(items, True)
