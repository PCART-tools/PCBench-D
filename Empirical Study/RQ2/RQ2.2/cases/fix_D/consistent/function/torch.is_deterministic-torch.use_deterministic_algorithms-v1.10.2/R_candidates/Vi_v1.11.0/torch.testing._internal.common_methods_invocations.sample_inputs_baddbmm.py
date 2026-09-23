def sample_inputs_baddbmm(op_info, device, dtype, requires_grad, **kwargs):
    test_cases = [((S, S, M), (S, S, S), (S, S, M), 1, 1, False),
                  ((1,), (S, S, S), (S, S, M), 1, 1, True),
                  ((S, S, M), (S, S, S), (S, S, M), 0.6, 0.2, False),
                  ((1,), (S, S, S), (S, S, M), 0.6, 0.2, True),
                  ((), (S, S, S), (S, S, M), 1, 1, True),
                  ((), (S, S, S), (S, S, M), 0.6, 0.2, True),
                  ]
    sample_inputs = []
    for (input_shape, batch1_shape, batch2_shape, alpha, beta, broadcasts_input) in test_cases:
        args = (make_tensor(input_shape, device, dtype,
                            low=None, high=None,
                            requires_grad=requires_grad),
                make_tensor(batch1_shape, device, dtype,
                            low=None, high=None,
                            requires_grad=requires_grad),
                make_tensor(batch2_shape, device, dtype,
                            low=None, high=None,
                            requires_grad=requires_grad))

        sample_inputs.append(SampleInput(args[0], args=(args[1], args[2]),
                             kwargs=dict(beta=beta, alpha=alpha), broadcasts_input=broadcasts_input))
        if dtype.is_complex:
            sample_inputs.append(SampleInput(
                args[0].clone().requires_grad_(requires_grad),
                args=(args[1].clone().requires_grad_(requires_grad),
                      args[2].clone().requires_grad_(requires_grad)),
                kwargs=dict(beta=beta * (1 + 2j), alpha=alpha * (2 + 3j)),
                broadcasts_input=broadcasts_input))

    if dtype.is_complex:
        shapes = [(S, S, S), (S, M, S), (S, S, M)]
        args = (make_tensor(shapes[0], device, dtype,
                            low=None, high=None,
                            requires_grad=requires_grad),
                make_tensor(shapes[1], device, dtype,
                            low=None, high=None,
                            requires_grad=requires_grad),
                make_tensor(shapes[2], device, dtype,
                            low=None, high=None,
                            requires_grad=requires_grad))
        sample_inputs.append(
            SampleInput(
                args[0].transpose_(-1, 1),
                args=(args[1].transpose(-1, 1).conj().requires_grad_(requires_grad),
                      args[2].transpose(-1, 1).conj().requires_grad_(requires_grad)),
                kwargs=dict(beta=beta * (1 + 2j), alpha=alpha * (2 + 3j)),))

    return tuple(sample_inputs)
