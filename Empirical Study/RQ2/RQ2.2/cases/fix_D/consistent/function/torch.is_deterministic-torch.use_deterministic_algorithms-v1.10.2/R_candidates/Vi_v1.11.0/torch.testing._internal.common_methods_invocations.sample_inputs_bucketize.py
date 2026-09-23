def sample_inputs_bucketize(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    sizes = ((), (S,), (S, S), (S, S, S), (S, 1, S), (S, 0, S))

    sample_inputs = []

    for size, out_int32, right in product(sizes, [False, True], [False, True]):
        input_tensor = make_arg(size)
        boundaries = make_arg((S,)).msort()

        sample_inputs.append(SampleInput(input_tensor, args=(boundaries, ),
                                         kwargs=dict(out_int32=out_int32, right=right)))

    return sample_inputs
