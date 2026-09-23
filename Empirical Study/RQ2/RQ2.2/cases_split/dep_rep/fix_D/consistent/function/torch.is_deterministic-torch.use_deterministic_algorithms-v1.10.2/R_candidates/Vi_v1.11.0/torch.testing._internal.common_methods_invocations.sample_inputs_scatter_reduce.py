def sample_inputs_scatter_reduce(op_info, device, dtype, requires_grad):
    def _tensor(shape, dtype=dtype, low=None, high=None):
        return make_tensor(shape, device, dtype, low=low, high=high, requires_grad=requires_grad)

    def _index(shape, max_index):
        return torch.from_numpy(np.random.choice(max_index, size=shape)).to(dtype=torch.int64, device=device)

    reduces = ["sum", "prod", "mean", "amax", "amin"]
    shapes_and_dims = [((M,), 1), ((M, S), 2), ((M, M, S), 3), ((1, M, M, S), 4)]

    sample_inputs = []

    for ((shape, dim), reduce) in itertools.product(shapes_and_dims, reduces):
        for d in range(dim):
            # Generate a random maximum integer that can appear in index array
            max_index = np.random.randint(1, shape[d] * 2)
            index = _index(shape, max_index)
            sample_inputs.append(
                SampleInput(
                    _tensor(shape),
                    args=(d, index, reduce),
                )
            )

    return sample_inputs
