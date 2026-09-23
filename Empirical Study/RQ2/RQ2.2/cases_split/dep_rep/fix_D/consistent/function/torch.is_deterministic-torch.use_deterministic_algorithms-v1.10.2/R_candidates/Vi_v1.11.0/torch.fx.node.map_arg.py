@compatibility(is_backward_compatible=True)
def map_arg(a: Argument, fn: Callable[[Node], Argument]) -> Argument:
    """
    Apply fn to each Node appearing arg. arg may be a list, tuple, slice, or dict with string keys.
    """
    assert callable(fn), "torch.fx.map_arg(a, fn): fn must be a callable"
    return map_aggregate(a, lambda x: fn(x) if isinstance(x, Node) else x)
