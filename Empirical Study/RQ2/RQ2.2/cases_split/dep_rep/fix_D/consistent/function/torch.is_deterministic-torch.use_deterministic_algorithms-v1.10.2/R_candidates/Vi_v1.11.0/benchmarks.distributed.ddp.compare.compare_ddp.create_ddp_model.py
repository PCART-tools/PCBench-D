def create_ddp_model(module, rank, pg, ddp_option, buffer_size_in_M):
    """Helper to create DDPModel. """
    if ddp_option == DDPOption.DDP_CPP_CORE:
        ddp_model = DDP(module, device_ids=[rank],
                        process_group=pg,
                        bucket_cap_mb=buffer_size_in_M)
        ddp_model._set_static_graph()
        return ddp_model
    elif ddp_option == DDPOption.PYTHON_DDP_SYNC_REDUCTION:
        M = 2 ** 20
        return python_ddp.PythonDDP(module, pg, False, buffer_size=buffer_size_in_M * M)
    elif ddp_option == DDPOption.PYTHON_DDP_ASYNC_REDUCTION:
        M = 2 ** 20
        return python_ddp.PythonDDP(module, pg, True, buffer_size=buffer_size_in_M * M)
    else:
        raise NotImplementedError
