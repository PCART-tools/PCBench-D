def barrier(group=GroupMember.WORLD, async_op=False, device_ids=None):

    """
    Synchronizes all processes.

    This collective blocks processes until the whole group enters this function,
    if async_op is False, or if async work handle is called on wait().

    Args:
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op
        device_ids ([int], optional): List of device/GPU ids.
                                      Valid only for NCCL backend.

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group
    """
    if _rank_not_in_group(group):
        return

    opts = BarrierOptions()
    if device_ids is not None:
        if get_backend(group) != Backend.NCCL:
            raise RuntimeError(
                "Function argument device_ids not supported "
                "for the selected backend {}".format(get_backend(group))
            )
        if isinstance(device_ids, list):
            opts.device_ids = device_ids
        else:
            raise RuntimeError(
                "Invalid function argument: " "device_ids type should be List[int]"
            )

    if group is None:
        default_pg = _get_default_group()
        work = default_pg.barrier(opts=opts)
    else:
        work = group.barrier(opts=opts)

    if async_op:
        return work
    else:
        work.wait()
