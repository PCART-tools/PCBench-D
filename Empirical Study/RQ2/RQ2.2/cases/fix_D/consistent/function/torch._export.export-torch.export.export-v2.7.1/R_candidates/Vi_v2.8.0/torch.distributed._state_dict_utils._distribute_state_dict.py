def _distribute_state_dict(
    full_state_dict: dict[str, Any],
    local_state_dict: dict[str, Any],
    device: torch.device,
    pg: Optional[dist.ProcessGroup] = None,
) -> None:
    # Full_state_dict = True, broadcast_from_rank0 = False here. Each rank has
    # full_state_dict. Skip the broadcast in ``_broadcast_state_dict`` and
    # distribute tensors in each rank
    for key, value in full_state_dict.items():
        if key not in full_state_dict:
            continue
        if not torch.is_tensor(value):
            local_state_dict[key] = value
        elif value.dim() == 0:
            local_state_dict[key] = value.cpu()
        else:
            assert isinstance(value, torch.Tensor)
            local_state = local_state_dict.get(key, None)
            if local_state is None:
                continue
            elif isinstance(local_state, DTensor):
                local_state_dict[key] = distribute_tensor(
                    value.detach().to(device),
                    local_state.device_mesh,
                    local_state.placements,
                )
            else:
                local_state_dict[key] = value.detach().to(device)
