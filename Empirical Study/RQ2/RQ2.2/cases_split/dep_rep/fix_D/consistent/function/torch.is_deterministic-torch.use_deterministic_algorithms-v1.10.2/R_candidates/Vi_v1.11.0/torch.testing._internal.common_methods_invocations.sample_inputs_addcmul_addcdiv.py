def sample_inputs_addcmul_addcdiv(op_info, device, dtype, requires_grad, **kwargs):
    test_cases = [(((S, S), (S, S), (S, S)), False),
                  (((S, S), (S, 1), (1, S)), False),
                  (((1,), (S, S, 1), (1, S)), True),
                  (((), (), ()), False),
                  (((S, S), (), ()), True),
                  (((), (S, S, 1), (1, S)), True)
                  ]

    sample_inputs = []
    for input_args, broadcasts_input in test_cases:
        args = tuple(make_tensor(arg, device, dtype, requires_grad=requires_grad) if isinstance(arg, tuple) else arg
                     for arg in input_args)
        sample_inputs.append(SampleInput(
            args[0],
            args=args[1:],
            broadcasts_input=broadcasts_input))

        args = tuple(make_tensor(arg, device, dtype, requires_grad=requires_grad) if isinstance(arg, tuple) else arg
                     for arg in input_args)
        sample_inputs.append(SampleInput(
            args[0],
            args=args[1:],
            kwargs=dict(value=3.14), broadcasts_input=broadcasts_input))

    return tuple(sample_inputs)
