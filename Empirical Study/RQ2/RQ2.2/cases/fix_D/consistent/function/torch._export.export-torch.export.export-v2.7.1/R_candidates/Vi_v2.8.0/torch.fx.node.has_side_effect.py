@compatibility(is_backward_compatible=False)
def has_side_effect(fn: Callable[_P, _R]) -> Callable[_P, _R]:
    _side_effectful_functions.add(fn)
    return fn
