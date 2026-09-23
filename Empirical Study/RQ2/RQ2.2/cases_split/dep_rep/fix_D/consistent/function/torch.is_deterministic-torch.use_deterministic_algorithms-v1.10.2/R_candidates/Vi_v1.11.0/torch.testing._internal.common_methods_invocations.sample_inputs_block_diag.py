def sample_inputs_block_diag(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    test_cases: Tuple[tuple] = (((1, S), (2, S), (3, S),),)

    samples: List[SampleInput] = []
    for shape, *other_shapes in test_cases:
        samples.append(SampleInput(make_arg(shape), args=tuple(make_arg(s) for s in other_shapes)))

    return samples
