def sample_inputs_pow(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype)

    samples = []

    if dtype in [torch.float16, torch.bfloat16, torch.float32, torch.float64]:
        test_cases = (
            ((2, 2), 0, 5, 1e-3, requires_grad, (2, 2), 0, 1, 0.1, requires_grad, False),
            ((2, 2), 0, 5, 1e-3, requires_grad, (1,), 0, 1, 0.1, requires_grad, False),
            ((), 1e-3, 1e-3 + 1, 0, requires_grad, (), 0.1, 1.1, 0, requires_grad, False),
            ((2, 2), 0, 5, 1e-3, requires_grad, (), 0.1, 1.1, 1, requires_grad, False),
        )
        tests_require_resizing = (
            ((1,), 0, 5, 1e-3, requires_grad, (2, 2), 0, 1, 0.1, requires_grad, requires_grad),
            ((2, 1, 2), 0, 5, 1e-3, requires_grad, (1, 2, 1), 0, 1, 0.1, requires_grad, requires_grad),
            ((), 1e-3, 1e-3 + 1, 0, requires_grad, (1, S, 1), 0, 1, 0.1, requires_grad, requires_grad),
        )
        cases = test_cases + tests_require_resizing

        samples = []
        for (shape_b, low_b, high_b, additive_b, b_grad, shape_e, low_e,
             high_e, additive_e, e_grad, broadcasts_input) in cases:
            si = SampleInput((make_arg(shape_b, low=low_b, high=high_b) + additive_b).requires_grad_(b_grad),
                             args=((make_arg(shape_e, low=low_e, high=high_e) + additive_e).requires_grad_(e_grad),),
                             broadcasts_input=broadcasts_input)
            samples.append(si)

        tensor_scalar_inputs = (
            ((2, 2), 0, 5, 1e-3, requires_grad, (3.14,)),
            ((), 1e-3, 1e-3 + 1, 0, requires_grad, (3.14,))
        )
        more_samples = list(SampleInput(
            (make_arg(shape, high=high, low=low) + additive).requires_grad_(b_grad),
            args=exp)
            for shape, low, high, additive, b_grad, exp in tensor_scalar_inputs)

        samples = [*samples, *more_samples]
    elif dtype in [torch.complex64, torch.complex128]:
        args_tuple = (
            ((2, 2), 0, 5, requires_grad, (3.14,)),
            ((), 0, 1, requires_grad, (3.14,)),
            ((), 0, 1, requires_grad, (3.14j,))
        )
        samples = list(SampleInput(
            (make_arg(shape, high=high, low=low) + 1e-3 * (1 + 1j)).requires_grad_(b_grad),
            args=arg)
            for shape, low, high, b_grad, arg in args_tuple)
    else:  # integral dtype
        exp_tuple = (1, 2, 3)
        samples = list(SampleInput(
            make_arg((2, 2), requires_grad=requires_grad),
            args=(arg,))
            for arg in exp_tuple)
        samples.append(SampleInput(
            make_arg((2, 2), requires_grad=requires_grad),
            args=(make_arg((2, 2), requires_grad=requires_grad),)))
    return tuple(samples)
