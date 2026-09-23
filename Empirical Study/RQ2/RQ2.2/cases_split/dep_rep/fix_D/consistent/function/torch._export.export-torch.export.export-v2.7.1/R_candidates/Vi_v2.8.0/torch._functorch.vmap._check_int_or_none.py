def _check_int_or_none(x, func, out_dims):
    if isinstance(x, int):
        return
    if x is None:
        return
    raise ValueError(
        f"vmap({_get_name(func)}, ..., out_dims={out_dims}): `out_dims` must be "
        f"an int, None or a python collection of ints representing where in the outputs the "
        f"vmapped dimension should appear."
    )
