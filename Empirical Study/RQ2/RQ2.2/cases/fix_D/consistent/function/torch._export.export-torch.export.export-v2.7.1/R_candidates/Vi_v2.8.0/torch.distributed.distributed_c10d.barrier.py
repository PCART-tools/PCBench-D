@_exception_logger
def barrier(
    group: Optional[ProcessGroup] = GroupMember.WORLD, async_op=False, device_ids=None
):
    """
    Synchronize all processes.

    This collective blocks processes until the whole group enters this function,
    if async_op is False, or if async work handle is called on wait().

    Args:
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op
        device_ids ([int], optional): List of device/GPU ids. Only one id is expected.

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group

    .. note:: `ProcessGroupNCCL` now blocks the cpu thread till the completion of the barrier collective.
    """
    group = group or _get_default_group()

    if _rank_not_in_group(group):
        _warn_not_in_group("barrier")
        return

    opts = BarrierOptions()
    opts.asyncOp = async_op
    # Detect the accelerator on the machine. If no accelerator is available, it
    # returns CPU.
    device = torch._C._get_accelerator()
    if isinstance(device_ids, list):
        opts.device_ids = device_ids
        # use only the first device id
        opts.device = torch.device(device.type, device_ids[0])
    elif getattr(group, "bound_device_id", None) is not None:
        # Use device id from `init_process_group(device_id=...)`
        opts.device = group.bound_device_id  # type: ignore[assignment]
    elif device.type == "cpu" or _get_object_coll_device(group) == "cpu":
        opts.device = torch.device("cpu")
    else:
        # Use the current device set by the user. If user did not set any, this
        # may use default device 0, causing issues like hang or all processes
        # creating context on device 0.
        opts.device = device
        warnings.warn(  # warn only once
            "No device id is provided via `init_process_group` or `barrier `. Using the current device set by the user. "
        )

    work = group.barrier(opts=opts)

    if async_op:
        return work
    elif (
        work is not None
    ):  # Backward compatible with backends that don't sync at CPP level
        work.wait()
