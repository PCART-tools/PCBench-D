def rendezvous(
    tensor: torch.Tensor, group: Union[str, "ProcessGroup"]
) -> _SymmetricMemory:
    r"""
    rendezvous(tensor, group) -> _SymmetricMemory

    Establish a symmetric memory tensor among participating processes. This is
    a collective operation.

    Args:
        tensor (:class:`torch.Tensor`): the local tensor used to establish the symmetric memory tensor.
            It must be allocated via :func:`torch._distributed._symmetric_memory.empty()`. The shape,
            dtype, and device type must be identical across all participating processes.
        group (Union[str, :class:`torch.distributed.ProcessGroup`]): The group identifying the
            participating processes. This can be either a group name or a process group object.
    """
    from torch._C._distributed_c10d import ProcessGroup

    if isinstance(group, str):
        group_name = group
    elif isinstance(group, ProcessGroup):
        group_name = group.group_name
    else:
        raise TypeError(f"rendezvous: unsupported group type: {type(group)}")

    enable_symm_mem_for_group(group_name)
    return _SymmetricMemory.rendezvous(tensor, group_name)
