@torch.no_grad()
def context_parallel_unshard(
    mesh: DeviceMesh,
    buffers: list[torch.Tensor],
    seq_dims: list[int],
) -> list[torch.Tensor]:
    """
    Unshard the tensors (e.g., output) that are sharded due to context parallelism.

    Args:
        mesh (:class:`DeviceMesh`): the device mesh for the context parallelism.
        buffers (List[torch.Tensor]): the buffers to be unsharded.
        seq_dims (List[int]): the sequence dimensions of ``buffers``. This list
            must have the same length as ``buffers``.

    Returns:
        List[torch.Tensor]: the unsharded buffers.
    """
    sharder = (
        _RoundRobinLoadBalancer
        if _cp_options.enable_load_balance
        else _SequentialSharder
    )
    return [sharder.unshard(b, mesh, dim) for b, dim in zip(buffers, seq_dims)]
