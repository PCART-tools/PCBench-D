def sample_inputs_index_add(op_info, device, dtype, requires_grad, **kwargs):
    # These testa are pretty much the same as those from index_copy.
    # Perhaps merge?
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    t = make_arg((S, S))
    s = make_arg((S, S))
    # non-contiguous target
    t_nonctg = t.transpose(0, 1)
    # non-contiguous source
    s_nonctg = s.transpose(0, 1)

    idx = make_arg((S,), dtype=torch.int64, low=0, high=S)
    idx_nonctg = make_arg((S,), dtype=torch.int64, low=0, high=S, noncontiguous=True)
    samples = [SampleInput(tensor, args=(1, idx, source))
               for tensor, idx, source in product([t, t_nonctg], [idx, idx_nonctg], [s, s_nonctg])]
    samples.extend(SampleInput(tensor, args=(1, idx, source), kwargs=dict(alpha=a))
                   for tensor, idx, source, a in product([t, t_nonctg], [idx, idx_nonctg], [s, s_nonctg], [-1, 0, 2]))

    # Add scalar cases
    scalar_sizes = [(), (1,)]
    ts = (make_arg(size) for size in scalar_sizes)
    idxs = (make_arg(size, dtype=torch.int64, low=0, high=1) for size in scalar_sizes)
    ss = (make_arg(size) for size in scalar_sizes)

    samples.extend(SampleInput(t, args=(0, idx, s)) for t, idx, s in product(ts, idxs, ss))
    samples.extend(SampleInput(t, args=(0, idx, s), kwargs=dict(alpha=a)) for t, idx, s, a in product(ts, idxs, ss, [-1, 0, 2]))
    return samples
