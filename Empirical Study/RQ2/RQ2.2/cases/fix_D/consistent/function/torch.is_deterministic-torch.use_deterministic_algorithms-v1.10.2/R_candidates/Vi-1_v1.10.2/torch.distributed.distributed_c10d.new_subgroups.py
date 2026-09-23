def new_subgroups(
    group_size=None,
    group=None,
    timeout=default_pg_timeout,
    backend=None,
    pg_options=None,
):
    """
    Creates GPU subgroups of equal size. By default, it creates intra-machine subgroups,
    where each of which contains all the ranks of a machine, based on the assumption
    that each machine has the same number of CUDA devices.

    This is a convenience API that calls ``new_group`` to generate multiple subgroups.
    It requires that all processes in the main group (i.e. all
    processes that are part of the distributed job) enter this function, even
    if they are not going to be members of the group.

    .. warning::
        This API only works when CUDA is available.

    .. warning::
        If ``group_size`` is passed in, the world size must be divisible by ``group_size``.
        If no ``group_size`` is passed in, and not all the machines have the same number
        of devices, the subgroup division will be different across nodes and can cause
        unexpected behaviors.

    .. warning::
        Using multiple process groups with the ``NCCL`` backend concurrently
        is not safe and the user should perform explicit synchronization in
        their application to ensure only one process group is used at a time.
        This means collectives from one process group should have completed
        execution on the device (not just enqueued since CUDA execution is
        async) before collectives from another process group are enqueued.
        See `Using multiple NCCL communicators concurrently <https://docs.nvid
        ia.com/deeplearning/nccl/user-guide/docs/usage/communicators.html#using
        -multiple-nccl-communicators-concurrently>`_ for more details.

    Args:
        group_size (int, optional): The size of each subgroup. If ``None``,
            the default subgroup size is equal to the number of devices on each machine,
            based on the assumption that each machine has exactly the same
            number of devices. Default is ``None``.
        timeout (timedelta, optional): Timeout for operations executed against
            the process group. Default value equals 30 minutes.
            This is applicable for the ``gloo`` backend. For ``nccl``, this is
            applicable only if the environment variable ``NCCL_BLOCKING_WAIT``
            or ``NCCL_ASYNC_ERROR_HANDLING`` is set to 1. When
            ``NCCL_BLOCKING_WAIT`` is set, this is the duration for which the
            process will block and wait for collectives to complete before
            throwing an exception. When ``NCCL_ASYNC_ERROR_HANDLING`` is set,
            this is the duration after which collectives will be aborted
            asynchronously and the process will crash. ``NCCL_BLOCKING_WAIT``
            will provide errors to the user which can be caught and handled,
            but due to its blocking nature, it has a performance overhead. On
            the other hand, ``NCCL_ASYNC_ERROR_HANDLING`` has very little
            performance overhead, but crashes the process on errors. This is
            done since CUDA execution is async and it is no longer safe to
            continue executing user code since failed async NCCL operations
            might result in subsequent CUDA operations running on corrupted
            data. Only one of these two environment variables should be set.
        backend (str or Backend, optional): The backend to use. Depending on
            build-time configurations, valid values are ``gloo`` and ``nccl``.
            By default uses the same backend as the global group. This field
            should be given as a lowercase string (e.g., ``"gloo"``), which can
            also be accessed via :class:`Backend` attributes (e.g.,
            ``Backend.GLOO``). If ``None`` is passed in, the backend
            corresponding to the default process group will be used. Default is
            ``None``.
        pg_options (ProcessGroupOptions, optional): process group options
            specifying what additional options need to be passed in during
            the construction of specific process groups. i.e. for the ``nccl``
            backend, ``is_high_priority_stream`` can be specified so that
            process group can pick up high priority cuda streams.

    Returns:
        The subgroup containing the current rank, and all the subgroups used for cleanup.

    Examples:
        >>> # Create intra-machine subgroups.
        >>> cur_subgroup, subgroups = dist.new_subgroups()
        >>> # Allreduce within the machine.
        >>> rank = dist.get_rank()
        >>> tensor = torch.ones(1, device=rank) * rank
        >>> dist.all_reduce(tensor, group=cur_subgroup)
        >>> tensor
        tensor([8])     # Assume 8 is the number of CUDA devices per machine.
        >>> # Cleanup.
        >>> for subgroup in subgroups:
        >>>     dist.destroy_process_group(subgroup)
    """
    if not torch.cuda.is_available():
        raise ValueError("Subgroups can only be created when CUDA is available")

    if group_size is None:
        group_size = torch.cuda.device_count()
    world_size = get_world_size()
    if world_size < group_size:
        raise ValueError("The arg 'group_size' must not exceed the world size")
    if world_size % group_size != 0:
        raise ValueError("The world size must be divisible by 'group_size'")

    subgroups = []
    cur_subgroup = None

    for subgroup_id in range(world_size // group_size):
        start_rank = subgroup_id * group_size
        end_rank = start_rank + group_size
        ranks_in_subgroup = list(range(start_rank, end_rank))
        subgroup = new_group(
            ranks=ranks_in_subgroup,
            timeout=timeout,
            backend=backend,
            pg_options=pg_options,
        )
        subgroups.append(subgroup)

        rank = get_rank()
        if rank in ranks_in_subgroup:
            cur_subgroup = subgroup
            logger.info(
                "Rank {} is assigned to subgroup {}".format(rank, ranks_in_subgroup)
            )

    return cur_subgroup, subgroups
