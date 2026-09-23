def _new_process_group_helper(
    world_size,
    rank,
    group_ranks,
    backend,
    store,
    pg_options=None,
    group_name=None,
    timeout=default_pg_timeout,
):
    """
    Create a new distributed process group.

    This function must be called by ALL processes in the global group, even if
    the calling process is not part of the newly created group. In that case,
    this function returns GroupMember.NON_GROUP_MEMBER.

    This function is called with ``group_ranks == []`` for the default group.
    """
    global _pg_map
    global _group_count
    global _pg_names

    if not group_name:
        group_name = str(_group_count)
        _group_count += 1

    if group_name in _pg_names.values():
        raise RuntimeError(
            "The specified group name has already been "
            "created, please use a different group name"
        )

    if not isinstance(timeout, timedelta):
        raise RuntimeError(
            "Expected timeout argument to be of type" "datetime.timedelta"
        )

    # The list of group ranks is empty if we're creating the default group.
    is_default_group = len(group_ranks) == 0

    backend = Backend(backend)
    pg: Union[ProcessGroupGloo, ProcessGroupMPI, ProcessGroupNCCL]
    if backend == Backend.MPI:
        if not is_mpi_available():
            raise RuntimeError(
                "Distributed package doesn't have MPI built in."
                " MPI is only included if you build PyTorch from"
                " source on a host that has MPI installed."
            )
        pg = ProcessGroupMPI.create(group_ranks)
        if not pg:
            return GroupMember.NON_GROUP_MEMBER
        _pg_map[pg] = (Backend.MPI, None)
        _pg_names[pg] = group_name
    else:
        # If this is a subgroup (which means group_ranks is specified),
        # we check if the current process is a member of the new group.
        if not is_default_group:
            global_rank = _get_default_group().rank()
            if global_rank not in group_ranks:
                return GroupMember.NON_GROUP_MEMBER

        # Use the group name as prefix in the default store, such that
        # a single store can be reused by multiple groups.
        prefix_store = PrefixStore(group_name, store)

        if backend == Backend.GLOO:
            if pg_options is not None:
                raise RuntimeError("GLOO options not supported")
            pg = ProcessGroupGloo(prefix_store, rank, world_size, timeout=timeout)
            # In debug mode and if GLOO is available, wrap in a wrapper PG that
            # enables enhanced collective checking for debugability.
            if get_debug_level() == DebugLevel.DETAIL:
                if not _GLOO_AVAILABLE:
                    logger.info(
                        """TORCH_DISTRIBUTED_DEBUG was set to DETAIL, but
                                GLOO is not available. Build with Gloo to
                                create a wrapper process group in debug mode
                                to aid collective desynchronization debugging."""
                    )
                else:
                    pg = _create_process_group_wrapper(
                        wrapped_pg=pg,
                        store_prefix=group_name,
                        store=store,
                        rank=rank,
                        world_size=world_size,
                        timeout=timeout,
                    )
            _pg_map[pg] = (Backend.GLOO, store)
            _pg_names[pg] = group_name
        elif backend == Backend.NCCL:
            if not is_nccl_available():
                raise RuntimeError("Distributed package doesn't have NCCL " "built in")
            if pg_options is not None:
                assert isinstance(
                    pg_options, ProcessGroupNCCL.Options
                ), "Expected pg_options argument to be of type ProcessGroupNCCL.Options"
            else:
                # default pg_options for NCCL
                pg_options = ProcessGroupNCCL.Options()
                pg_options.is_high_priority_stream = False
                pg_options._timeout = timeout

            pg = ProcessGroupNCCL(prefix_store, rank, world_size, pg_options)
            # In debug mode and if GLOO is available, wrap in a wrapper PG that
            # enables enhanced collective checking for debugability.
            if get_debug_level() == DebugLevel.DETAIL:
                if not _GLOO_AVAILABLE:
                    logger.info(
                        """TORCH_DISTRIBUTED_DEBUG was set to DETAIL, but
                                GLOO is not available. Build with Gloo to
                                create a wrapper process group in debug mode
                                to aid collective desynchronization debugging."""
                    )
                else:
                    pg = _create_process_group_wrapper(
                        wrapped_pg=pg,
                        store_prefix=group_name,
                        store=store,
                        rank=rank,
                        world_size=world_size,
                        timeout=timeout,
                    )
            _pg_map[pg] = (Backend.NCCL, store)
            _pg_names[pg] = group_name
        else:
            assert backend.upper() in Backend._plugins, (
                f"unknown c10d backend type {backend.upper()}"
            )
            pg = Backend._plugins[backend.upper()](
                prefix_store, rank, world_size, timeout
            )
            _pg_map[pg] = (backend, store)
            _pg_names[pg] = group_name

    return pg
