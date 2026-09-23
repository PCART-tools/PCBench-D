def sample_inputs_linalg_norm(op_info, device, dtype, requires_grad, **kwargs):
    test_sizes = [
        (S,),
        (0,),
        (S, S),
        (0, 0),
        (S, 0),
        (0, S),
        (S, S, S),
        (0, S, S),
        (S, 0, S),
        (0, 0, 0),
    ]

    vector_ords = (None, 0, 0.5, 1, 2, 3.5, inf, -0.5, -1, -2, -3.5, -inf)
    matrix_ords = (None, 'fro', 'nuc', 1, 2, inf, -1, -2, -inf)

    inputs = []

    for test_size in test_sizes:
        is_vector_norm = len(test_size) == 1
        is_matrix_norm = len(test_size) == 2

        for keepdim in [False, True]:
            inputs.append(SampleInput(
                make_tensor(
                    test_size, device, dtype, low=None, high=None,
                    requires_grad=requires_grad),
                kwargs=dict(
                    keepdim=keepdim)))

            if not (is_vector_norm or is_matrix_norm):
                continue

            ords = vector_ords if is_vector_norm else matrix_ords

            for ord in ords:

                inputs.append(SampleInput(
                    make_tensor(
                        test_size, device, dtype,
                        low=None, high=None,
                        requires_grad=requires_grad),
                    args=(ord,),
                    kwargs=dict(
                        keepdim=keepdim)))

                if ord in ['nuc', 'fro']:
                    inputs.append(SampleInput(
                        make_tensor(
                            test_size, device, dtype,
                            low=None, high=None,
                            requires_grad=requires_grad),
                        kwargs=dict(
                            ord=ord,
                            keepdim=keepdim,
                            dim=(0, 1))))
        return inputs
