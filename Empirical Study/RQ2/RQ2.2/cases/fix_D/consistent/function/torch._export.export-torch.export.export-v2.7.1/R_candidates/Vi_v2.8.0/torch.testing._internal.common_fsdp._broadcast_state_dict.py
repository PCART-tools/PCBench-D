def _broadcast_state_dict(rank, state_dict):
    # For non-FSDP roots, some parts of the model state on rank 0 may
    # not be on CPU, so we move everything to CPU to avoid issues like:
    # https://github.com/pytorch/pytorch/issues/77113.
    for param_name, param in state_dict.items():
        if param.device != torch.device("cpu"):
            state_dict[param_name] = param.cpu()

    olist = [state_dict if rank == 0 else None]
    dist.broadcast_object_list(olist)
    state_dict = cast(dict[str, torch.Tensor], olist[0])
    # Ensure that the state is on DEVICE
    for param_name in state_dict.keys():
        state_dict[param_name] = state_dict[param_name].to(DEVICE_TYPE)
    return state_dict
