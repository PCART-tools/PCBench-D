def sample_inputs_softmax_variant(op_info, device, dtype, requires_grad, with_dtype=False, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    cases = [
        ((S, ), (0, )),
        ((S, S), (0, )),
        ((S, S), (1, )),
        ((S, S), (-1, )),
        ((S, M, S), (2, )),
    ]

    # PyTorch on XLA throws an error when passed with dim argument for 0d tensor.
    # See https://github.com/pytorch/xla/issues/3061 for more details.
    if torch.device(device).type != 'xla':
        cases.append(((), (0, )))

    return [
        SampleInput(make_arg(shape), args=dim, kwargs=dict(dtype=torch.float64) if with_dtype else None)
        for shape, dim in cases
    ]
