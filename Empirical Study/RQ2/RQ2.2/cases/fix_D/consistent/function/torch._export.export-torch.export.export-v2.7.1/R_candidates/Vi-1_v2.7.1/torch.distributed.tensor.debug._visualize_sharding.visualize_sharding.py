def visualize_sharding(dtensor, header=""):
    """
    Visualizes sharding in the terminal for :class:`DTensor` that are 1D or 2D.

    .. note:: This requires the ``tabulate`` package. No sharding info will be printed for empty tensors
    """
    if dtensor.numel() == 0:  # we do not print for empty dtensors
        return

    if len(dtensor.shape) >= 3:
        raise RuntimeError(
            "visualize sharding is only implemented for 1D or 2D dtensor"
        )
    placements = dtensor.placements
    device_mesh = dtensor.device_mesh
    device_type = dtensor.device_mesh.device_type

    if device_mesh.get_coordinate() is None:  # current rank is not in the mesh
        return

    # Only display the visualization once for each DTensor, on the rank whose
    # coordinate is 0 on all dimensions. For example, if the mesh is a full mesh,
    # we will only print on rank 0.
    local_rank_zero_on_all_dim = all(
        device_mesh.get_local_rank(mesh_dim=dim) == 0 for dim in range(device_mesh.ndim)
    )
    if not local_rank_zero_on_all_dim:
        return

    device_map = _mesh_to_coordinate(device_mesh, device_type)
    all_offsets = []
    for device in device_map:
        local_shape, global_offset = _compute_local_shape_and_global_offset(
            dtensor.shape, device_mesh, placements, device_map[device]
        )
        all_offsets.append([local_shape, global_offset, device])

    # Convert offsets to blocks with row_ranges for tabulate
    blocks = _convert_offset_to_ranges(all_offsets)

    # Print the table
    print(header)
    print(_create_table(blocks))
