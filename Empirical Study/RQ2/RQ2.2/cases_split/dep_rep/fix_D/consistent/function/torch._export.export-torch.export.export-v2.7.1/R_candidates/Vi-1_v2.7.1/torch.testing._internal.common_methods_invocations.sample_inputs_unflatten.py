def sample_inputs_unflatten(op_info, device, dtype, requires_grad, **kwargs):
    # in_shape, dim, sizes
    args = (((8,), 0, (8,)),
            ((8,), 0, (4, 2)),
            ((8,), -1, (2, 2, 2)),
            ((8,), -1, (-1, 2)),
            ((3, 6, 2), 1, (2, 3)),
            ((3, 6, 2), -2, (2, 3)),
            ((3, 6, 2), -2, (-1, 3)),
            ((3, 2, 12), 2, (3, 2, 2)),
            ((4, 0), 0, (2, 2)),
            ((4, 0), 1, (2, 0, 0, 0)),
            )
    make_tensor_partial = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    for in_shape, dim, sizes in args:
        yield SampleInput(make_tensor_partial(in_shape), args=(dim, sizes))
