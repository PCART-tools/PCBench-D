def _init_process_group(store, rank, world_size):
    # Initialize ProcessGroup.
    process_group_timeout = rpc_constants.DEFAULT_PROCESS_GROUP_TIMEOUT

    # We're using a bunch of private APIs here since `new_group` requires the
    # default group to be initialized.
    group = dist.ProcessGroupGloo(store, rank, world_size, process_group_timeout)

    assert group is not None, "Failed to initialize default ProcessGroup."

    if (rank != -1) and (rank != group.rank()):
        raise RuntimeError(
            "rank argument {} doesn't match pg rank {}".format(rank, group.rank())
        )
    if (world_size != -1) and (world_size != group.size()):
        raise RuntimeError(
            "world_size argument {} doesn't match pg size {}".format(
                world_size, group.size()
            )
        )
    return group
