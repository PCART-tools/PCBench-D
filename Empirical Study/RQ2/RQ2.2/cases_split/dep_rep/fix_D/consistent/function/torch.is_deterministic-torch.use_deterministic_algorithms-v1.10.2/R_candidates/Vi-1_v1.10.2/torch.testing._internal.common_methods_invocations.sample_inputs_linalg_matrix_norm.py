def sample_inputs_linalg_matrix_norm(op_info, device, dtype, requires_grad, **kwargs):
    sizes = ((2, 2), (2, 3, 2))
    ords = ('fro', 'nuc', inf, -inf, 1, -1, 2, -2)
    dims = ((-2, -1), (-1, 0))

    inputs: List[SampleInput] = []
    for size, ord, dim, keepdim in product(sizes, ords, dims, [True, False]):
        t = make_tensor(size, device, dtype, requires_grad=requires_grad)
        inputs.append(SampleInput(t, args=(ord, dim, keepdim)))

    return inputs
