@_time_logger
def split_group(
    parent_pg: Optional[ProcessGroup] = None,
    split_ranks: Optional[list] = None,
    timeout: Optional[timedelta] = None,
    pg_options: Optional[Any] = None,
    group_desc: Optional[str] = None,
) -> Optional[ProcessGroup]:
    """
    Create a new process group split from the given parent process group.

    warning:: This is an experimental API. Only the ``NCCL`` and custom plugin backends
    are supported. Other backends will raise an error.
    Users of this API must guarantee that all ranks in the parent group enter this API call,
    and the split of the sub groups is the same across all ranks in the parent group.

    Args:
        parent_pg (ProcessGroup, optional): The parent process group. If None,
            the default process group will be used. Users need to guarantee that
            the parent group is fully initialized (e.g, communicators are initialized)
        split_ranks (list[list[int]]): the split ranks, which is a list of list of ranks.
            Users need to make sure the validity of the split ranks such that one
            split (represented by one inner list of ints) does not overlap with any other split.
            Note that the ranks in each split is the group rank (instead of global rank)
            in the parent pg. For example, if the parent group has 4 ranks, and split_ranks can be
            [[0, 1], [2, 3]]. Note [[0,1]] is also a valid split, in which case ranks 2, 3 would
            return a non-group member.
        timeout (timedelta, optional): see `init_process_group` for details and default value.
        pg_options (ProcessGroupOptions, optional): Additional options need to be passed in during
            the construction of specific process groups. i.e.``is_high_priority_stream``
            can be specified so that process group can pick up high priority cuda streams.
        group_desc (str, optional): a string to describe the process group.

    Returns:
        ProcessGroup if the current rank is within one split/subgroup given by split_ranks,
        or None if the current rank is not part of any split_ranks`.

    """
    # check inputs
    if split_ranks is None:
        raise ValueError("split_ranks cannot be None")

    global _world
    default_pg = _get_default_group()
    device_id = default_pg.bound_device_id
    if not device_id:
        raise RuntimeError(
            "No device associated with the default pg, not safe to split any process groups"
        )
    _default_backend, default_store = _world.pg_map[default_pg]
    global_rank = default_pg.rank()
    global_world_size = default_pg.size()

    if not parent_pg:
        parent_pg = default_pg
    if parent_pg not in _world.pg_group_ranks:
        raise ValueError(f"Group {parent_pg} is not registered")

    parent_global_to_group_ranks = _world.pg_group_ranks[parent_pg]
    parent_group_to_global_ranks = {
        group_rank: global_rank
        for global_rank, group_rank in parent_global_to_group_ranks.items()
    }

    if global_rank not in parent_global_to_group_ranks:
        raise ValueError(
            f"Global rank {global_rank} is not part of the parent group {parent_pg}"
        )

    parent_group_rank = parent_global_to_group_ranks[global_rank]
    parent_backend = parent_pg._get_backend(torch.device("cuda"))

    # if the parent backend does not support splitting, raise error
    # currently this API only support NCCL backend
    if not parent_backend or not parent_backend.supports_splitting:
        raise RuntimeError(
            "No backend for the parent process group or its backend does not support splitting"
        )

    # set the group_desc before the color or no_cloor split
    group_desc = (
        f"{parent_pg.group_desc}:split:{parent_backend.comm_split_count()}"  # type: ignore[attr-defined]
        if group_desc is None
        else group_desc
    )

    parent_backend_str, _ = _world.pg_map[parent_pg]
    # same type of backend as the parent process group
    backend = Backend(parent_backend_str)
    backend_config = BackendConfig(backend)

    if pg_options is None:
        # default pg_options same as the parent process group
        pg_options = parent_backend.options

    # this timeout defaulting/validation is used for all the new_groups/new_subgroups variants,
    # which may just pass their timeout value (or None)
    if timeout is None:
        timeout = _get_default_timeout(backend)
    _check_valid_timeout(timeout)

    # find my group of ranks and my group local rank in split_ranks
    my_group = None
    group_rank = -1

    for split_group in split_ranks:
        if len(split_group) == 0:
            raise ValueError("the split group cannot be empty")
        if len(split_group) > global_world_size:
            raise ValueError(
                "the split group's size should be less or equal to the world_size set by init_process_group"
            )
        if len(split_group) != len(set(split_group)):
            raise ValueError("the split group cannot have duplicate ranks")
        split_group = sorted(split_group)
        if parent_group_rank in split_group:
            my_group = split_group
            group_rank = split_group.index(parent_group_rank)
            break
    # if my rank does not belong to any sub group,
    # no_color split should be called
    if my_group is None or group_rank == -1:
        parent_backend.perform_nocolor_split(device_id)  # type: ignore[attr-defined]
        return None

    group_name = _process_group_name(my_group, use_hashed_name=False)
    global_ranks_in_my_group = [parent_group_to_global_ranks[rank] for rank in my_group]

    prefix_store = PrefixStore(f"{group_name}/", default_store)
    # We register the backend after initializing and timeout is set in pg_options.
    pg: ProcessGroup = ProcessGroup(
        prefix_store,
        group_rank,
        len(my_group),
    )
    pg.bound_device_id = device_id  # type: ignore[union-attr]
    pg_options._timeout = timeout  # type: ignore[union-attr]
    pg_options.split_from = parent_backend  # type: ignore[union-attr]
    pg_options.split_color = _process_group_color(my_group)  # type: ignore[union-attr]
    pg_options.global_ranks_in_group = global_ranks_in_my_group  # type: ignore[union-attr]
    pg_options.group_name = group_name  # type: ignore[union-attr]

    if parent_backend_str == Backend.NCCL:
        backend_type = ProcessGroup.BackendType.NCCL
        if not isinstance(pg_options, ProcessGroupNCCL.Options):
            raise RuntimeError(
                "Expected pg_options argument to be of type ProcessGroupNCCL.Options"
            )
        backend_class = ProcessGroupNCCL(
            prefix_store, group_rank, len(my_group), pg_options
        )
    else:
        assert parent_backend_str.upper() in Backend._plugins, (
            f"Unknown c10d backend type {parent_backend_str.upper()}"
        )
        backend_plugin = Backend._plugins[parent_backend_str.upper()]
        creator_fn = backend_plugin.creator_fn
        extended_api = backend_plugin.extended_api
        backend_type = ProcessGroup.BackendType.CUSTOM
        if not extended_api:
            backend_class = creator_fn(prefix_store, group_rank, len(my_group), timeout)
        else:
            dist_backend_opts = _DistributedBackendOptions()
            dist_backend_opts.store = prefix_store
            dist_backend_opts.group_rank = group_rank
            dist_backend_opts.group_size = len(my_group)
            backend_class = creator_fn(dist_backend_opts, pg_options)

    pg._set_default_backend(backend_type)
    backend_class._set_sequence_number_for_group()

    pg._register_backend(torch.device("cuda"), backend_type, backend_class)

    # set group_name and group_desc to backend
    assert group_name is not None
    assert group_desc is not None
    pg._set_group_name(group_name)
    pg._set_group_desc(group_desc)

    # always eagerly initialize the backend in split_group
    eager_backend = pg._get_backend(device_id)
    eager_backend.eager_connect_single_device(device_id)

    # update global state
    _world.pg_map[pg] = (backend, prefix_store)
    _world.pg_names[pg] = group_name
    _register_process_group(group_name, pg)
    _world.pg_backend_config[pg] = str(backend_config)
    pg_tag = f"ptd:{group_name}"
    _world.tags_to_pg.setdefault(pg_tag, []).append(pg)
    _world.pg_to_tag[pg] = pg_tag

    # Create the global rank to group rank mapping
    _world.pg_group_ranks[pg] = {
        global_rank: group_rank
        for group_rank, global_rank in enumerate(global_ranks_in_my_group)
    }

    return pg
