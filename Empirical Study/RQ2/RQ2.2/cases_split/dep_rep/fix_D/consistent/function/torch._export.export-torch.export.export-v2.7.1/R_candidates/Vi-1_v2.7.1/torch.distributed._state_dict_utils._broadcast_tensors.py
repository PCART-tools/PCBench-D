def _broadcast_tensors(
    full_state_dict: dict[str, Any],
    local_state_dict: dict[str, Any],
    keys: list[str],
    device: torch.device,
    pg: Optional[dist.ProcessGroup] = None,
) -> None:
    tensors = []
    for key in keys:
        if dist.get_rank() == 0:
            full_state = full_state_dict[key]
            assert isinstance(full_state, torch.Tensor)
            full_tensor = full_state.detach().to(device)
        else:
            tensor_info = full_state_dict[key]
            full_tensor = torch.empty(
                size=tensor_info.size,
                device=device,
                dtype=tensor_info.dtype,
            )
        tensors.append(full_tensor)
        local_state = local_state_dict.get(key, None)
        if local_state is None:
            continue
        elif isinstance(local_state, DTensor):
            local_state_dict[key] = (local_state, full_tensor)
        else:
            local_state_dict[key] = full_tensor

    if pg is None:
        pg = dist.distributed_c10d._get_default_group()

    if len(tensors) > 1:
        dist._broadcast_coalesced(pg, tensors, 500, 0)
    else:
        dist.broadcast(tensors[0], src=0, group=pg)

    _distribute_tensors(local_state_dict, keys, device, pg)
