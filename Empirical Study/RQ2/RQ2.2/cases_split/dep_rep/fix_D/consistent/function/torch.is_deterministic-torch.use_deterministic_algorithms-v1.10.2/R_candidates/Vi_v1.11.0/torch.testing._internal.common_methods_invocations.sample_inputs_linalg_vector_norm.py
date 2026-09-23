def sample_inputs_linalg_vector_norm(op_info, device, dtype, requires_grad, **kwargs):
    size_1D = (S,)
    size_2D = (2, 2)

    test_cases = [
        # input size, ord, dim args
        (size_1D, 2, None),
        (size_1D, 2, (0,)),
        (size_1D, 0, None),
        (size_1D, 0, (0,)),
        (size_1D, 0.9, None),
        (size_1D, 0.9, (0,)),
        (size_1D, 1, None),
        (size_1D, 1, (0,)),
        (size_1D, -2.1, None),
        (size_1D, -2.1, (0,)),
        (size_1D, inf, None),
        (size_1D, inf, (0,)),
        (size_1D, -inf, None),
        (size_1D, -inf, (0,)),

        (size_2D, 2, None),
        (size_2D, 2, (0,)),
        (size_2D, 2, (-1, 0)),
        (size_2D, 0, None),
        (size_2D, 0, (0,)),
        (size_2D, 0, (-1, 0)),
        (size_2D, 0.9, None),
        (size_2D, 0.9, (0,)),
        (size_2D, 0.9, (-1, 0)),
        (size_2D, 1, None),
        (size_2D, 1, (0,)),
        (size_2D, 1, (-1, 0)),
        (size_2D, -2.1, None),
        (size_2D, -2.1, (0,)),
        (size_2D, -2.1, (-1, 0)),
        (size_2D, inf, None),
        (size_2D, inf, (0,)),
        (size_2D, inf, (-1, 0)),
        (size_2D, -inf, None),
        (size_2D, -inf, (0,)),
        (size_2D, -inf, (-1, 0)),
    ]
    inputs = []

    for test_size, ord, dim in test_cases:
        for keepdim in [False, True]:
            inputs.append(SampleInput(
                make_tensor(
                    test_size, device, dtype,
                    low=None, high=None,
                    requires_grad=requires_grad),
                args=(ord,),
                kwargs=dict(
                    keepdim=keepdim,
                    dim=dim)))

    return inputs
