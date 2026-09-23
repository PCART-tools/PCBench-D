@compatibility(is_backward_compatible=True)
def map_aggregate(a: ArgumentT, fn: Callable[[Argument], Argument]) -> ArgumentT:
    """
    Apply fn recursively to each object appearing in arg.

    arg may be a list, tuple, slice, or dict with string keys: the return value will
    have the same type and structure.
    """
    return _fx_map_aggregate(a, fn)
