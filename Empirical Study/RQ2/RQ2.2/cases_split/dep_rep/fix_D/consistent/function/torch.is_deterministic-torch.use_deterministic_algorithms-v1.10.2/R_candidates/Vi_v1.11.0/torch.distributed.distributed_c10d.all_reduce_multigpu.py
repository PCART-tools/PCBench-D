def all_reduce_multigpu(tensor_list, op=ReduceOp.SUM, group=None, async_op=False):
    r"""
    Reduces the tensor data across all machines in such a way that all get
    the final result. This function reduces a number of tensors on every node,
    while each tensor resides on different GPUs.
    Therefore, the input tensor in the tensor list needs to be GPU tensors.
    Also, each tensor in the tensor list needs to reside on a different GPU.

    After the call, all ``tensor`` in ``tensor_list`` is going to be bitwise
    identical in all processes.

    Complex tensors are supported.

    Only nccl and gloo backend is currently supported
    tensors should only be GPU tensors

    Args:
        tensor_list (List[Tensor]): List of input and output tensors of
            the collective. The function operates in-place and requires that
            each tensor to be a GPU tensor on different GPUs.
            You also need to make sure that ``len(tensor_list)`` is the same for
            all the distributed processes calling this function.
        op (optional): One of the values from
            ``torch.distributed.ReduceOp``
            enum.  Specifies an operation used for element-wise reductions.
        group (ProcessGroup, optional): The process group to work on. If
            ``None``, the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group

    """
    if _rank_not_in_group(group):
        return

    tensor_list = [
        t if not t.is_complex() else torch.view_as_real(t) for t in tensor_list
    ]

    opts = AllreduceOptions()
    opts.reduceOp = op
    if group is None:
        default_pg = _get_default_group()
        work = default_pg.allreduce(tensor_list, opts)
    else:
        work = group.allreduce(tensor_list, opts)

    if async_op:
        return work
    else:
        work.wait()
