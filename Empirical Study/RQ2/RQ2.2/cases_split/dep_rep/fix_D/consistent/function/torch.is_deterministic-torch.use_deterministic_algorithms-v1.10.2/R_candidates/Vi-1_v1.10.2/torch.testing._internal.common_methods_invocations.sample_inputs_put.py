def sample_inputs_put(op_info, device, dtype, requires_grad):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    make_idx = partial(make_tensor, low=0, dtype=torch.int64, device=device, requires_grad=False)

    S = 3

    def gen_inputs():
        # Generic inputs
        tgt_gen = (make_arg((S, S), noncontiguous=not ctg) for ctg in (True, False))
        src_gen = (make_arg((S,), noncontiguous=not ctg) for ctg in (True, False))
        idx = torch.randperm(S * S, device=device, dtype=torch.int64)[:S]
        idx_nonctg = torch.repeat_interleave(idx, 2, dim=-1)[::2]
        idx_neg = -idx - 1
        idx_list = [idx, idx_nonctg, idx_neg]
        for tgt, idx, src, acc in product(tgt_gen, idx_list, src_gen, (True, False)):
            yield SampleInput(input=tgt, args=(idx, src, acc))

        # Scalar cases
        scalar_sizes = [(), (1,)]
        tgt_gen = (make_arg(size) for size in scalar_sizes)
        idx_gen = (make_idx(size, high=1) for size in scalar_sizes)
        src_gen = (make_arg(size) for size in scalar_sizes)
        for tgt, idx, src, acc in product(tgt_gen, idx_gen, src_gen, (True, False)):
            yield SampleInput(input=tgt, args=(idx, src, acc))

        # Empty cases
        tgt_sizes = [(0,), (), (1,), (3, 2)]
        tgt_gen = (make_arg(size) for size in tgt_sizes)
        idx = make_idx((0,), high=1)
        src = make_arg((0,))
        for tgt, acc in product(tgt, (True, False)):
            yield SampleInput(input=tgt, args=(idx, src, acc))

    return list(gen_inputs())
