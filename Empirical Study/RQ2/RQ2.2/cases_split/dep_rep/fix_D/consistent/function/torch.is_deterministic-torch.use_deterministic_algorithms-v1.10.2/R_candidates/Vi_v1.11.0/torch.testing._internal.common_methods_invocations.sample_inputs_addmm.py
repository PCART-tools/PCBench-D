def sample_inputs_addmm(op_info, device, dtype, requires_grad, **kwargs):
    alpha_val = kwargs.get('alpha', 2 + 3j if dtype.is_complex else 0.6)
    beta_val = kwargs.get('beta', 1 + 2j if dtype.is_complex else 0.2)
    tests_list = [
        ((2, 3), (2, 2), (2, 3), False)
    ]
    tests_with_lhs_broadcasting = [
        ((1,), (2, 2), (2, 3), True),
        ((), (2, 2), (2, 3), True)
    ]
    test_cases = tests_list + tests_with_lhs_broadcasting  # type: ignore[operator]

    sample_inputs = []

    for shape_a, shape_b, shape_c, broadcasts_input in test_cases:
        sample_inputs.append(
            SampleInput(
                make_tensor(shape_a, device, dtype, requires_grad=requires_grad),
                args=(
                    make_tensor(shape_b, device, dtype,
                                requires_grad=requires_grad),
                    make_tensor(shape_c, device, dtype,
                                requires_grad=requires_grad)),
                kwargs={'alpha': alpha_val, 'beta': beta_val},
                broadcasts_input=broadcasts_input))

    if dtype.is_complex:
        shape = (3, 3)
        sample_inputs.append(
            SampleInput(make_tensor(shape, device, dtype, requires_grad=requires_grad),
                        args=(
                            make_tensor(shape, device, dtype).mH.requires_grad_(requires_grad),
                            make_tensor(shape, device, dtype,
                                        requires_grad=requires_grad)),
                        kwargs={'alpha': alpha_val, 'beta': beta_val},))
        sample_inputs.append(
            SampleInput(make_tensor(shape, device, dtype, requires_grad=requires_grad),
                        args=(
                            make_tensor(shape, device, dtype,
                                        requires_grad=requires_grad),
                            make_tensor(shape, device, dtype).mH.requires_grad_(requires_grad)),
                        kwargs={'alpha': alpha_val, 'beta': beta_val},))
    return sample_inputs
