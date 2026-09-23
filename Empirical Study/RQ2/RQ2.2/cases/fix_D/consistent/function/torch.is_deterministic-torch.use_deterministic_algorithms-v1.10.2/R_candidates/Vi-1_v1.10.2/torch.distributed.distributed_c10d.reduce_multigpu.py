def reduce_multigpu(
    tensor_list, dst, op=ReduceOp.SUM, group=None, async_op=False, dst_tensor=0
):
    """
    Reduces the tensor data on multiple GPUs across all machines. Each tensor
    in ``tensor_list`` should reside on a separate GPU

    Only the GPU of ``tensor_list[dst_tensor]`` on the process with rank ``dst``
    is going to receive the final result.

    Only nccl backend is currently supported
    tensors should only be GPU tensors

    Args:
        tensor_list (List[Tensor]): Input and output GPU tensors of the
            collective. The function operates in-place.
            You also need to make sure that ``len(tensor_list)`` is the same for
            all the distributed processes calling this function.
        dst (int): Destination rank
        op (optional): One of the values from
            ``torch.distributed.ReduceOp``
            enum.  Specifies an operation used for element-wise reductions.
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op
        dst_tensor (int, optional): Destination tensor rank within
                                    ``tensor_list``

    Returns:
        Async work handle, if async_op is set to True.
        None, otherwise

    """
    if _rank_not_in_group(group):
        return

    opts = ReduceOptions()
    opts.reduceOp = op
    opts.rootRank = dst
    opts.rootTensor = dst_tensor

    if group is None or group is GroupMember.WORLD:
        default_pg = _get_default_group()
        work = default_pg.reduce(tensor_list, opts)
    else:
        group_dst_rank = _get_group_rank(group, dst)
        opts.rootRank = group_dst_rank
        work = group.reduce(tensor_list, opts)

    if async_op:
        return work
    else:
        work.wait()
