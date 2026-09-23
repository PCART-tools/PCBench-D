def _faulty_tensorpipe_init_backend_handler(
    store, name, rank, world_size, rpc_backend_options
):
    from . import FaultyTensorPipeAgent
    from . import FaultyTensorPipeRpcBackendOptions
    from torch.distributed.rpc import api

    if not isinstance(store, dist.Store):
        raise TypeError("`store` must be a c10d::Store. {}".format(store))

    if not isinstance(
        rpc_backend_options, FaultyTensorPipeRpcBackendOptions
    ):
        raise TypeError(
            "`rpc_backend_options` must be a `FaultyTensorPipeRpcBackendOptions`. {}".format(
                rpc_backend_options
            )
        )

    agent = FaultyTensorPipeAgent(
        store,
        name,
        rank,
        world_size,
        rpc_backend_options,
        {},  # reverse_device_map
        [],  # devices
    )
    api._init_rpc_states(agent)

    return agent
