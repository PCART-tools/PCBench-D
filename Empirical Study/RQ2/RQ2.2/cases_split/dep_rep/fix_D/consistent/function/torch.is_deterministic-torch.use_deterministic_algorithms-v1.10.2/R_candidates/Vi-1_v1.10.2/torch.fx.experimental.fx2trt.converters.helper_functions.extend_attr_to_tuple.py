def extend_attr_to_tuple(mod: torch.nn.Module, name: str, size: int):
    """
    Extend an attribute of `mod` that named `name` to a tuple of `size`.
    """
    val = getattr(mod, name)
    if not isinstance(val, tuple):
        val = (val,) * size
    return val
