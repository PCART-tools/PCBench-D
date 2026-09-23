def all_to_all(tensors, group=dist.group.WORLD):
    """
    Each process scatters list of input tensors to all processes in a group and
    return gathered list of tensors in output list.

    Arguments:
        tensors (list[Tensor]): List of tensors to scatter one per rank.
        group (ProcessGroup, optional): The process group to work on.

    Returns:
        tuple[Tensor]): Output of the collective.

    """
    return _AlltoAll.apply(group, *tensors)
