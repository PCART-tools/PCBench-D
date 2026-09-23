@compatibility(is_backward_compatible=False)
def has_side_effect(fn: Callable) -> Callable:
    _side_effectful_functions.add(fn)
    return fn
