def extend_mod_attr_to_tuple(mod: torch.nn.Module, name: str, size: int):
    """
    Extend an attribute of `mod` that named `name` to a tuple of `size`.
    """
    val = getattr(mod, name)
    return extend_attr_to_tuple(val, size)
