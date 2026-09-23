def sample_inputs_index(op_info, device, dtype, requires_grad, **kwargs):
    # target.index_select(dim, idx)
    select = op_info.name == "index_select"
    # target.index_add(dim, idx, source, *, alpha=1)
    add = op_info.name == "index_add"
    # target.index_copy(dim, idx, source)
    copy = op_info.name == "index_copy"
    # target.index_fill(dim, idx, value)
    fill = op_info.name == "index_fill"

    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_permutation = partial(torch.randperm, device=device, dtype=torch.int64)

    def make_idx(n):
        return make_tensor((n,), device=device, dtype=torch.int64, low=0, high=n)

    shapes = [(), (1,), (S, S)]
    # extra parameter for add
    alphas = (-1, 0, 2) if add else (None,)

    for shape, alpha in product(shapes, alphas):
        t = make_arg(shape)
        args = []

        # dim. We handle the scalar case
        dim = 1 if t.ndim == 2 else 0
        args.append(dim)

        # idx They need to be different for copy and add to be deterministic
        make_idx_fn = make_permutation if copy or add else make_idx
        idx = make_idx_fn(t.shape[dim] if t.ndim != 0 else 1)
        args.append(idx)

        # source
        if copy or add:
            args.append(make_arg(shape))
        elif fill:
            # A weird number to catch errors
            args.append(make_arg((1,)).item())

        args = tuple(args)
        kwargs = {} if alpha is None else {"alpha": alpha}

        yield SampleInput(t, args=args, kwargs=kwargs)
