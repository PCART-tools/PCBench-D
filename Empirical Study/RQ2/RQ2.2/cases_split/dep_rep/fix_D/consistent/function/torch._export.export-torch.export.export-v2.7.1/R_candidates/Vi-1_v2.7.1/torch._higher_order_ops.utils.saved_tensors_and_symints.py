def saved_tensors_and_symints(ctx):
    args = []
    t_idx = 0
    s_idx = 0
    saved_tensors = ctx.saved_tensors
    for p in ctx.pos:
        if p == 0:
            args.append(saved_tensors[t_idx])
            t_idx += 1
        else:
            args.append(ctx.sym_int_args[s_idx])
            s_idx += 1
    assert t_idx + s_idx == len(ctx.pos)
    return tuple(args)
