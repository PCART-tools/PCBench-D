def Dim(name: str, *, min: Optional[int] = None, max: Optional[int] = None):
    """
    :func:`Dim` constructs a type analogous to a named symbolic integer with a range.
    It can be used to describe multiple possible values of a dynamic tensor dimension.
    Note that different dynamic dimensions of the same tensor, or of different tensors,
    can be described by the same type.

    Args:
        name (str): Human-readable name for debugging.
        min (Optional[int]): Minimum possible value of given symbol (inclusive)
        max (Optional[int]): Maximum possible value of given symbol (inclusive)

    Returns:
        A type that can be used in dynamic shape specifications for tensors.
    """

    from torch.utils._sympy.numbers import int_oo

    _min = 0 if min is None else min
    _max = int_oo if max is None else max
    assert _max > _min, f"Cannot create Dim with inconsistent min={min}, max={max}"
    assert name.isidentifier(), f"Dim name must be a valid identifier, got {name}"
    dim = _Dim(name, (int,), {"min": _min, "max": _max})
    dim.__module__ = getattr(
        inspect.getmodule(inspect.stack()[1][0]), "__name__", "__main__"
    )
    return dim
