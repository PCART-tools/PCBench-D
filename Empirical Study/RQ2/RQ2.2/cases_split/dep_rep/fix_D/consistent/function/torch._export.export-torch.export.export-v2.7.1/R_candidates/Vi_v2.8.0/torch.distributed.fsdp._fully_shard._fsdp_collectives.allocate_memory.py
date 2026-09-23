def allocate_memory(
    size: int,
    dtype: torch.dtype,
    device: torch.device,
    group: dist.ProcessGroup,
    from_process_group: bool,
) -> torch.Tensor:
    if from_process_group:
        backend = group._get_backend(device)
        if backend.supports_tensor_alloc(device):
            return backend.allocate_tensor(size, dtype=dtype, device=device)
    return torch.empty((size,), dtype=dtype, device=device)
