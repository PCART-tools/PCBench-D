def sample_repeat_tile(op_info, device, dtype, requires_grad, **kwargs):
    rep_dims = ((), (0, ), (1, ), (0, 2), (1, 1), (2, 3), (2, 3, 2), (0, 2, 3), (2, 1, 1, 1),)
    shapes = ((), (0,), (2,), (3, 0), (3, 2), (3, 0, 1))

    if requires_grad:
        # Tests for variant_consistency_jit, grad, gradgrad
        # are slower. Use smaller bags of `rep_dims` and `shapes`
        # in this case.
        rep_dims = ((), (0, ), (0, 2), (1, 1), (2, 3), (1, 3, 2), (3, 1, 1))  # type: ignore[assignment]
        shapes = ((), (0,), (2,), (3, 2))  # type: ignore[assignment]

    tensors = [make_tensor(shape, device, dtype,
                           low=None, high=None,
                           requires_grad=requires_grad) for shape in shapes]

    samples = []
    for rep_dim, tensor in product(rep_dims, tensors):
        for t in (tensor, tensor.T):
            if op_info.name == 'repeat' and len(rep_dim) >= t.dim():
                # `torch.repeat` errors for `len(rep_dims) < t.dim()`,
                # so we filter such combinations.
                samples.append(SampleInput(t, args=(rep_dim,),))
            elif op_info.name == 'tile':
                samples.append(SampleInput(t, args=(rep_dim,),))

    return samples
