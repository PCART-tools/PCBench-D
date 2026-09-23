def save_tensors_and_symints_for_backward(ctx, args):
    assert all(
        isinstance(arg, (torch.Tensor, torch.SymInt, int, type(None))) for arg in args
    ), args
    partitioned_args: list[Any] = [[], []]
    pos = []
    for arg in args:
        idx = 0 if isinstance(arg, torch.Tensor) else 1
        partitioned_args[idx].append(arg)
        pos.append(idx)

    assert not hasattr(ctx, "sym_int_args"), "ctx already has sym_int_args attribute."
    assert not hasattr(ctx, "pos"), "ctx already has pos attribute."
    ctx.save_for_backward(*partitioned_args[0])
    ctx.sym_int_args = partitioned_args[1]
    ctx.pos = pos
