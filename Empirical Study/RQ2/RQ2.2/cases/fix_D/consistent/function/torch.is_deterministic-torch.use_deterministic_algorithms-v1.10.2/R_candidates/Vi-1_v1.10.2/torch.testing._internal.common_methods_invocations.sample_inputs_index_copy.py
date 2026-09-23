def sample_inputs_index_copy(op_info, device, dtype, requires_grad, **kwargs):
    def make_arg(shape, low=None, high=None, dtype=dtype):
        return make_tensor(shape, device=device, dtype=dtype,
                           low=low, high=high,
                           requires_grad=requires_grad)

    t = make_arg((S, S))
    s = make_arg((S, S))
    # non-contiguous input
    t01 = t.transpose(0, 1)
    # non-contiguous input
    s01 = s.transpose(0, 1)

    # idx is a permutation of 0...S-1 for this function to be deterministic
    idx = torch.randperm(S, device=device, dtype=torch.int64)
    # non-contiguous index
    idx_nonctg = torch.repeat_interleave(idx, 2, dim=-1)[::2]
    # index_copy_ does not support negative indices
    # idx_neg = -idx - 1
    samples = [SampleInput(tensor, args=(1, idx, source))
               for tensor, idx, source in product([t, t01], [idx, idx_nonctg], [s, s01])]

    # Add scalar cases
    scalar_sizes = [(), (1,)]
    ts = (make_arg(size) for size in scalar_sizes)
    idxs = (make_arg(size, dtype=torch.int64, low=0, high=1) for size in scalar_sizes)
    ss = (make_arg(size) for size in scalar_sizes)

    samples.extend(SampleInput(t, args=(0, idx, s)) for t, idx, s in product(ts, idxs, ss))
    return samples
