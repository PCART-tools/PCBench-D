def sample_inputs_tensorsolve(op_info, device, dtype, requires_grad, **kwargs):
    a_shapes = [(2, 3, 6), (3, 4, 4, 3)]
    # Zero-dim tensors are not supported in NumPy, so we skip them for now.
    # NumPy is used in reference check tests.
    # See https://github.com/numpy/numpy/pull/20482 for tracking NumPy bugfix.
    # a_shapes += [(0, 0, 1, 2, 3, 0)]
    dimss = [None, (0, 2)]

    for a_shape, dims in itertools.product(a_shapes, dimss):
        a = make_tensor(a_shape, dtype=dtype, device=device, requires_grad=requires_grad)
        b = make_tensor(a_shape[:2], dtype=dtype, device=device, requires_grad=requires_grad)
        yield SampleInput(a, args=(b,), kwargs=dict(dims=dims))
