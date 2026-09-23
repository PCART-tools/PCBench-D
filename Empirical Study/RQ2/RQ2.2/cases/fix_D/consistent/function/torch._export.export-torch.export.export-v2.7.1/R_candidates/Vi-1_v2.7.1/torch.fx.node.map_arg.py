@compatibility(is_backward_compatible=True)
def map_arg(a: ArgumentT, fn: Callable[[Node], Argument]) -> ArgumentT:
    """
    Apply fn recursively to each Node appearing in arg.

    arg may be a list, tuple, slice, or dict with string keys: the return value will
    have the same type and structure.
    """
    assert callable(fn), "torch.fx.map_arg(a, fn): fn must be a callable"
    return _fx_map_arg(a, fn)
