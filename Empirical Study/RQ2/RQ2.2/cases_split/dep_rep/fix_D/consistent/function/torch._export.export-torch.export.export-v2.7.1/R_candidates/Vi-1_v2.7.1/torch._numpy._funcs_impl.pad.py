def pad(array: ArrayLike, pad_width: ArrayLike, mode="constant", **kwargs):
    if mode != "constant":
        raise NotImplementedError
    value = kwargs.get("constant_values", 0)
    # `value` must be a python scalar for torch.nn.functional.pad
    typ = _dtypes_impl.python_type_for_torch(array.dtype)
    value = typ(value)

    pad_width = torch.broadcast_to(pad_width, (array.ndim, 2))
    pad_width = torch.flip(pad_width, (0,)).flatten()

    return torch.nn.functional.pad(array, tuple(pad_width), value=value)
