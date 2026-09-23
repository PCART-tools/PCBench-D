def _view_unbacked_meta(a, shape, size_oblivious_enabled=True):
    from torch.fx.experimental.symbolic_shapes import guard_or_false, sym_eq

    # Creates a valid shape
    shape = utils.extract_shape_from_varargs(shape, validate=False)

    # Reshape may be given a shape with a -1 length
    # This indicates that the dimension's length should be inferred
    shape = utils.infer_size(shape, a.numel())

    # Special-cases reshaping zero dim tensors
    if a.ndim == 0:
        _a = a
        for length in shape:
            torch._check(length == 1)
            _a = torch._refs.unsqueeze(_a, -1)
        if _a is a:
            return view_of(a)
        else:
            return _a

    # Special-cases reshaping to zero dim tensors
    if len(shape) == 0:
        _a = a
        for length in a.shape:
            torch._check(length == 1)
            _a = torch._refs.squeeze(_a, -1)
        if _a is a:
            return view_of(a)
        else:
            return _a

    shape_numel = reduce(operator.mul, shape, 1)

    torch._check(
        a.numel() == shape_numel,
        lambda: f"Could not reshape a tensor with shape {a.shape} as a tensor with shape {shape}!",
    )

    if len(shape) == len(a.shape) and guard_or_false(sym_eq(shape, a.shape)):
        return view_of(a)

    if definitely_contiguous(a) if size_oblivious_enabled else is_contiguous(a):
        strides = utils.make_contiguous_strides_for(shape)
        return a.as_strided(shape, strides)

    new_strides = _compute_stride(
        a.size(), a.stride(), shape, size_oblivious=size_oblivious_enabled
    )

    if new_strides is not None:
        return a.as_strided(shape, new_strides)

    # If we fail to do size oblivious view, and backed_size_oblivious was on,
    # then we redo everything by looking at hints and guarding instead of failing.
    # Also if the expression has unbacked symbols, then we run again with size_oblivious_enabled=False
    # to throw a data dependent error.

    if size_oblivious_enabled and (
        torch.fx.experimental._config.backed_size_oblivious
        or _view_has_unbacked_input(a, shape)
    ):
        return _view_unbacked_meta(a, shape, size_oblivious_enabled=False)

    msg = f"Cannot view a tensor with shape {a.shape} and strides {a.stride()} as a tensor with shape {shape}!"
    raise ValueError(msg)
