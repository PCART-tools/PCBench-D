def _transform_index(index, func):
    """
    Apply function to all values found in index.

    This includes transforming multiindex entries separately.

    """
    if isinstance(index, MultiIndex):
        items = [tuple(func(y) for y in x) for x in index]
        return MultiIndex.from_tuples(items, names=index.names)
    else:
        items = [func(x) for x in index]
        return Index(items, name=index.name)
