def _all_gather_dtensor(
    tensor: DTensor,
    parent_mesh: Optional[DeviceMesh],
) -> torch.Tensor:
    """All gather a DTensor in its FSDP dimension and return the local tensor."""
    assert parent_mesh == tensor.device_mesh

    placements = list(copy.deepcopy(tensor.placements))
    # FSDP + TP: [Shard(0), tp_placement] -> [Replicate(), tp_placement]
    # HSDP + TP: [Replicate(), Shard(0), tp_placement] -> [Replicate(), Replicate(), tp_placement]
    for i in range(0, len(placements) - 1):
        placements[i] = Replicate()
    tensor = tensor.redistribute(
        device_mesh=tensor.device_mesh,
        placements=placements,
    )

    return tensor.to_local()
