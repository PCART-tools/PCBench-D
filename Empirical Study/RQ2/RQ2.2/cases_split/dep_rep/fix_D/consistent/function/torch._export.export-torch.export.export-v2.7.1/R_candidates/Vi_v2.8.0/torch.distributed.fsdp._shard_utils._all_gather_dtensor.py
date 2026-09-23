def _all_gather_dtensor(
    tensor: DTensor,
    root_mesh: Optional[DeviceMesh],
) -> torch.Tensor:
    """
    All gather a DTensor in its sharded dimension and return the local tensor.
    """
    assert root_mesh == tensor.device_mesh, (
        "The device mesh of a tensor should be a root mesh."
    )

    placements = list(copy.deepcopy(tensor.placements))
    # FSDP placements: [Shard(0)] -> [Replicate()]
    # HSDP placements: [Replicate(), Shard(0)] -> [Replicate(), Replicate()]
    placements[-1] = Replicate()
    tensor = tensor.redistribute(
        device_mesh=tensor.device_mesh,
        placements=placements,
    )

    return tensor.to_local()
