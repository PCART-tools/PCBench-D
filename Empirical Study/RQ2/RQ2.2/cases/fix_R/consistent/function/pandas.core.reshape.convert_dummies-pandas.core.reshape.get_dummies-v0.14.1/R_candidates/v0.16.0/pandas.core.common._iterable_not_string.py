def _iterable_not_string(x):
    return (isinstance(x, collections.Iterable) and
            not isinstance(x, compat.string_types))
