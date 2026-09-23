def _reduce_scatter_base(output, input, op=ReduceOp.SUM, group=None, async_op=False):
    """
    Reduces, then scatters a flattened tensor to all processes in a group.

    Args:
        output (Tensor): Output tensor.
        input (Tensor): Input tensor that is of size output tensor size times world size
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op.

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group.

    """
    _check_single_tensor(output, "output")
    _check_single_tensor(input, "input")

    if _rank_not_in_group(group):
        return

    opts = ReduceScatterOptions()
    opts.reduceOp = op

    if group is None:
        default_pg = _get_default_group()
        work = default_pg._reduce_scatter_base(output, input, opts)
    else:
        work = group._reduce_scatter_base(output, input, opts)

    if async_op:
        return work
    else:
        work.wait()
