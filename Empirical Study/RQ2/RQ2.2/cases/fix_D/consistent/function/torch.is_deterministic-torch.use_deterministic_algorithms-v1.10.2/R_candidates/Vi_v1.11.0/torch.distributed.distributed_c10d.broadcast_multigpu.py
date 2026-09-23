def broadcast_multigpu(tensor_list, src, group=None, async_op=False, src_tensor=0):
    """
    Broadcasts the tensor to the whole group with multiple GPU tensors
    per node.

    ``tensor`` must have the same number of elements in all the GPUs from
    all processes participating in the collective. each tensor in the list must
    be on a different GPU

    Only nccl and gloo backend are currently supported
    tensors should only be GPU tensors

    Args:
        tensor_list (List[Tensor]): Tensors that participate in the collective
            operation. If ``src`` is the rank, then the specified ``src_tensor``
            element of ``tensor_list`` (``tensor_list[src_tensor]``) will be
            broadcast to all other tensors (on different GPUs) in the src process
            and all tensors in ``tensor_list`` of other non-src processes.
            You also need to make sure that ``len(tensor_list)`` is the same
            for all the distributed processes calling this function.

        src (int): Source rank.
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op
        src_tensor (int, optional): Source tensor rank within ``tensor_list``

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group

    """
    if _rank_not_in_group(group):
        _warn_not_in_group("broadcast_multigpu")
        return

    opts = BroadcastOptions()
    opts.rootRank = src
    opts.rootTensor = src_tensor

    if group is None or group is GroupMember.WORLD:
        default_pg = _get_default_group()
        work = default_pg.broadcast(tensor_list, opts)
    else:
        group_src_rank = _get_group_rank(group, src)
        opts.rootRank = group_src_rank
        work = group.broadcast(tensor_list, opts)
    if async_op:
        return work
    else:
        work.wait()
