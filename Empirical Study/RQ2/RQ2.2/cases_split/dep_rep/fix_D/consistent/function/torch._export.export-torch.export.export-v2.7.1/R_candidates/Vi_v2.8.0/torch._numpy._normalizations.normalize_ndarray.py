def normalize_ndarray(arg, parm=None):
    # check the arg is an ndarray, extract its tensor attribute
    if arg is None:
        return arg

    from ._ndarray import ndarray

    if not isinstance(arg, ndarray):
        raise TypeError(f"'{parm.name}' must be an array")
    return arg.tensor
