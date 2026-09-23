def sample_inputs_index_fill(op_info, device, dtype, requires_grad, **kwargs):
    samples = []
    t = make_tensor((S, S, S), device, dtype,
                    low=None, high=None,
                    requires_grad=requires_grad)
    fill_val = torch.tensor(-1 + 1j if t.is_complex() else -1)
    # non-contiguous input
    t01 = t.transpose(0, 1)
    t02 = t.transpose(0, 2)
    t12 = t.transpose(1, 2)
    idx = index_variable(1, S, device=device)
    # non-contiguous index
    idx_nonctg = torch.empty_strided((S,), (2,), device=device, dtype=torch.int64)
    idx_nonctg.copy_(idx)
    for d in range(t.dim()):
        for tensor in [t, t01, t02, t12]:
            samples.append(SampleInput(tensor, args=(d, idx, fill_val)))
            samples.append(SampleInput(tensor, args=(d, -idx - 1, fill_val)))
            samples.append(SampleInput(tensor, args=(d, idx_nonctg, fill_val)))

    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    index_tensor = partial(torch.tensor, device=device, dtype=torch.long)

    def unique_idx(numel, max_idx):
        # Generate unique random indices vector of `numel`
        # elements in range [0, max_idx).
        indices = random.sample(range(max_idx), numel)
        return index_tensor(indices)

    samples.append(SampleInput(make_arg((S, S)), args=(0, unique_idx(2, S), 2)))
    samples.append(SampleInput(make_arg((S, S)), args=(0, unique_idx(2, S), make_arg(()))))
    samples.append(SampleInput(make_arg((S, S)), args=(0, index_tensor(0), 2)))
    samples.append(SampleInput(make_arg(()), args=(0, index_tensor([0]), 2)))
    samples.append(SampleInput(make_arg(()), args=(0, index_tensor(0), 2)))

    # Duplicate indices
    samples.append(SampleInput(make_arg((S, S)), args=(0, index_tensor([0, 0]), 2)))
    samples.append(SampleInput(make_arg((S, S)), args=(0, index_tensor([0, 0, 2]), make_arg(()))))

    return samples
