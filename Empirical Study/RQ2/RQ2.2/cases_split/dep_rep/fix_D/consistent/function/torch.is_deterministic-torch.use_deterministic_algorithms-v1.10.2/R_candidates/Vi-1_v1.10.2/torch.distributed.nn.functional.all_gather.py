def all_gather(tensor, group=dist.group.WORLD):
    """
    Gathers tensors from the whole group in a list.

    Arguments:
        tensor (Tensor): Tensor to be broadcast from current process.
        group (ProcessGroup, optional): The process group to work on.

    Returns:
        tuple[Tensor]): Output of the collective.

    """
    return _AllGather.apply(group, tensor)
