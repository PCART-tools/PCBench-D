def sample_inputs_pow(op_info, device, dtype, requires_grad, **kwargs):
    samples = []

    if dtype in [torch.float16, torch.bfloat16, torch.float32, torch.float64]:
        test_cases = (
            ((2, 2), 0, 5, 1e-3, requires_grad, (2, 2), 0, 1, 0.1, requires_grad, False),
            ((2, 2), 0, 5, 1e-3, requires_grad, (1,), 0, 1, 0.1, requires_grad, False),
            ((), 1e-3, 1e-3 + 1, 0, requires_grad, (), 0.1, 1.1, 0, False, False),
            ((2, 2), 0, 5, 1e-3, requires_grad, (), 0.1, 1.1, 1, False, False),
        )
        tests_require_resizing = (
            ((1,), 0, 5, 1e-3, requires_grad, (2, 2), 0, 1, 0.1, requires_grad, requires_grad),
            ((2, 1, 2), 0, 5, 1e-3, requires_grad, (1, 2, 1), 0, 1, 0.1, requires_grad, requires_grad),
            ((), 1e-3, 1e-3 + 1, 0, requires_grad, (1, S, 1), 0, 1, 0.1, requires_grad, requires_grad),
        )
        cases = test_cases + tests_require_resizing
        samples = list(SampleInput(make_tensor(shape_b, low=low_b, high=high_b,
                                               requires_grad=b_grad, device=device,
                                               dtype=dtype) + additive_b,
                                   args=(make_tensor(shape_e, low=low_e, high=high_e,
                                                     requires_grad=e_grad, device=device,
                                                     dtype=dtype) + additive_e,),
                                   broadcasts_input=broadcasts_input)
                       for shape_b, low_b, high_b, additive_b, b_grad, shape_e, low_e,
                       high_e, additive_e, e_grad, broadcasts_input in cases)
        tensor_scalar_inputs = (
            ((2, 2), 0, 5, 1e-3, requires_grad, (3.14,)),
            ((), 1e-3, 1e-3 + 1, 0, requires_grad, (3.14,))
        )
        more_samples = list(SampleInput(make_tensor(shape, dtype=dtype, device=device,
                                                    high=high, low=low,
                                                    requires_grad=b_grad) + additive,
                                        args=exp)
                            for shape, low, high, additive, b_grad, exp in tensor_scalar_inputs)
        samples = [*samples, *more_samples]
    elif dtype in [torch.complex64, torch.complex128]:
        args_tuple = (
            ((2, 2), 0, 5, requires_grad, (3.14,)),
            ((), 0, 1, requires_grad, (3.14,)),
            ((), 0, 1, requires_grad, (3.14j,))
        )
        samples = list(SampleInput(make_tensor(shape, dtype=dtype, device=device,
                                               high=high, low=low,
                                               requires_grad=b_grad) + 1e-3 * (1 + 1j),
                                   args=arg)
                       for shape, low, high, b_grad, arg in args_tuple)
    elif dtype == torch.bool:
        arg_tuple = (0, 1, 1., 2.3)
        samples = list(SampleInput(make_tensor((2, 2), device=device, dtype=dtype,
                                               requires_grad=requires_grad),
                                   args=(arg,))
                       for arg in arg_tuple)
        dtypes_list = [torch.float64, torch.float32, torch.int64, torch.int32]
        more_samples = list(SampleInput(make_tensor((2, 2), device, dtype=torch.bool,
                                                    requires_grad=requires_grad),
                                        args=(make_tensor((2, 2), device, dtype=dtype,
                                                          requires_grad=requires_grad),))
                            for dtype in dtypes_list)
        samples = [*samples, *more_samples]
        samples.append(SampleInput(make_tensor((2, 2, 2), device, dtype=torch.bool,
                                               requires_grad=requires_grad),
                                   args=(make_tensor((2, 1), device, dtype=torch.float64,
                                                     requires_grad=requires_grad),)))
    else:
        exp_tuple = (1, 2, 3)
        samples = list(SampleInput(make_tensor((2, 2), device, dtype,
                                               requires_grad=requires_grad),
                                   args=(arg,))
                       for arg in exp_tuple)
        samples.append(SampleInput(make_tensor((2, 2), device, dtype,
                                               requires_grad=requires_grad),
                                   args=(make_tensor((2, 2), device, dtype,
                                                     requires_grad=requires_grad),)))
    return tuple(samples)
