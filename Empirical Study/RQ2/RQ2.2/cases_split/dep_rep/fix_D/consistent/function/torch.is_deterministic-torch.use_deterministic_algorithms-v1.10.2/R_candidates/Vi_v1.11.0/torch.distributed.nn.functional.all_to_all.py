def all_to_all(output_tensor_list, input_tensor_list, group=dist.group.WORLD):
    """
    Each process scatters list of input tensors to all processes in a group and
    return gathered list of tensors in output list.

    Arguments:
        out_tensor_list (list[Tensor]): list of tensors to gather one per rank.
        input_tensor_list (list[Tensor]): List of tensors to scatter one per rank.
        group (ProcessGroup, optional): The process group to work on.

    Returns:
        tuple([Tensor]): Output of the collective.

    """
    return _AlltoAll.apply(group, output_tensor_list, *input_tensor_list)
