@compatibility(is_backward_compatible=True)
def map_aggregate(a: Argument, fn: Callable[[Argument], Argument]) -> Argument:
    """
    Apply fn to each Node appearing arg. arg may be a list, tuple, slice, or dict with string keys.
    """
    if isinstance(a, tuple):
        return tuple(map_aggregate(elem, fn) for elem in a)
    elif isinstance(a, list):
        return immutable_list(map_aggregate(elem, fn) for elem in a)
    elif isinstance(a, dict):
        return immutable_dict((k, map_aggregate(v, fn)) for k, v in a.items())
    elif isinstance(a, slice):
        return slice(map_aggregate(a.start, fn), map_aggregate(a.stop, fn), map_aggregate(a.step, fn))
    else:
        return fn(a)
