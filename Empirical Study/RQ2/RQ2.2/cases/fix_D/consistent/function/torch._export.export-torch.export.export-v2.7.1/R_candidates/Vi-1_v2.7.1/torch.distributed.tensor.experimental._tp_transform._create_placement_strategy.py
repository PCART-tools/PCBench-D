def _create_placement_strategy(
    node: Node,
    mesh: DeviceMesh,
    placements: tuple[Placement, ...],
    input_specs: Optional[Sequence[DTensorSpec]] = None,
) -> PlacementStrategy:
    """
    Util function to construct a placement strategy for a given node.
    """
    placement = PlacementStrategy(
        input_specs=input_specs,
        output_specs=DTensorSpec(
            mesh=mesh,
            placements=placements,
        ),
    )
    _populate_tensor_meta(node, placement.output_specs)
    return placement
