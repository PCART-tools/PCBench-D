def _context_parallel_buffers(
    mesh: DeviceMesh,
    buffers: list[torch.Tensor],
    buffer_seq_dims: list[int],
) -> list[torch.Tensor]:
    """Shard the buffers along the sequence dimensions according to CP rules."""
    new_buffers = []
    sharder = (
        _RoundRobinLoadBalancer
        if _cp_options.enable_load_balance
        else _SequentialSharder
    )
    for buffer, seq_dim in zip(buffers, buffer_seq_dims):
        new_buffers.append(sharder.shard(buffer, mesh, seq_dim))

    return new_buffers
