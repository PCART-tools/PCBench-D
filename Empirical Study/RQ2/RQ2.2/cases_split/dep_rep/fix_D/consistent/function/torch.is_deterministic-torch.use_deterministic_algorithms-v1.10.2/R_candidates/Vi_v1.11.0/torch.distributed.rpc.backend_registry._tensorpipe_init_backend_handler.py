def _tensorpipe_init_backend_handler(store, name, rank, world_size, rpc_backend_options):
    from . import TensorPipeRpcBackendOptions
    from . import TensorPipeAgent

    if not isinstance(store, dist.Store):
        raise TypeError("`store` must be a c10d::Store. {}".format(store))

    if not isinstance(
        rpc_backend_options, TensorPipeRpcBackendOptions
    ):
        raise TypeError(
            "`rpc_backend_options` must be a `TensorPipeRpcBackendOptions`. {}".format(
                rpc_backend_options
            )
        )

    # The agent's join method is required to behave like a barrier and perform
    # collective operations, for which it relies on a process group, instead of
    # re-implementing this on top of RPCs.

    group = _init_process_group(store, rank, world_size)

    if torch.cuda.is_available():
        # It's necessary to initialize PyTorch CUDA states here (e.g.,
        # CUDACachingAllocator). If this is missing, we could hit errors like
        # "allocator not initialized", because other processes might send
        # CUDA-related RPC request to this process before user code in this
        # process initializes its PyTorch CUDA states.
        torch.cuda.init()
        device_count = torch.cuda.device_count()
    else:
        device_count = 0

    reverse_device_maps, devices = _tensorpipe_exchange_and_check_all_device_maps(
        name,
        device_count,
        rpc_backend_options.device_maps,
        rpc_backend_options.devices,
        group,
    )

    # TODO: add try-except and destroy _agent in all processes if any fails.
    agent = TensorPipeAgent(
        store,
        name,
        rank,
        world_size,
        rpc_backend_options,
        reverse_device_maps,
        devices,
    )

    api._init_rpc_states(agent)

    # Run one dummy round of RPC to initialize channels/transports. Without
    # this, it's easy to hit timeout in rpc.shutdown() if there is no other RPC
    # on that process before rpc.shutdown(), as the agent initialization can
    # take longer than 5s.
    api._all_gather(None, timeout=rpc_backend_options.rpc_timeout)
    # Need a barrier here to make sure no peers leave before the rank0 finishes
    # _all_gather
    group.barrier().wait()

    return agent
