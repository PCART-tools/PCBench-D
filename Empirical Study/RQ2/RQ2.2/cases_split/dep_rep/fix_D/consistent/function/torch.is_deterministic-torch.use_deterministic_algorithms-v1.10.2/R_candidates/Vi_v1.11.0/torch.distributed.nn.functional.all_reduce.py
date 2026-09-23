def all_reduce(tensor, op=dist.ReduceOp.SUM, group=dist.group.WORLD):
    """
    Reduces the tensor data across all machines in such a way that all get
    the final result.

    After the call the returned tensor is going to be bitwise
    identical in all processes.

    Arguments:
        tensor (Tensor): Input of the collective.
        op (optional): One of the values from
            ``torch.distributed.ReduceOp``
            enum.  Specifies an operation used for element-wise reductions.
        group (ProcessGroup, optional): The process group to work on.

    Returns:
        Tensor: Output of the collective

    """
    return _AllReduce.apply(op, group, tensor)
