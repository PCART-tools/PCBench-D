def sample_inputs_linalg_matrix_power(op_info, device, dtype, requires_grad):
    # (<matrix_size>, (<batch_sizes, ...>))
    test_sizes = [
        (1, ()),
        (2, (0,)),
        (2, (2,)),
    ]

    inputs = []
    for matrix_size, batch_sizes in test_sizes:
        size = batch_sizes + (matrix_size, matrix_size)
        for n in (0, 3, 5):
            t = make_tensor(size, device, dtype, requires_grad=requires_grad)
            inputs.append(SampleInput(t, args=(n,)))
        for n in [-4, -2, -1]:
            t = random_fullrank_matrix_distinct_singular_value(matrix_size, *batch_sizes, device=device, dtype=dtype)
            t.requires_grad = requires_grad
            inputs.append(SampleInput(t, args=(n,)))

    return inputs
