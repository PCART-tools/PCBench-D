def _explicit_order_placements(
    mesh_shape: ShapeType, placements: Sequence[Placement]
) -> Sequence[tuple[int, Placement]]:
    """
    Replace Strided Shards with regular shards in an adjusted order.

    Returns a list of (mesh_dim, placement) tuples where the list order is the sharding order.

    ex.
    [Shard(0), _StridedShard(0, split_factor=2), Shard(0)] ->
    [(0, Shard(0)), (2, Shard(0)), (1, Shard(0))]

    """
    if not len(placements) == len(mesh_shape):
        raise RuntimeError(
            "Expected one placement per mesh dim, "
            f"but found {len(placements)} placements and {len(mesh_shape)} mesh dims."
        )
    ordered = []
    deferred_strided_placements = defaultdict(list)
    strided_part_ended_for_dim = set()
    for mesh_dim, p in enumerate(placements):
        if isinstance(p, _StridedShard):
            # validate the stride is the correct multiple of the meshdim and the earlier shard
            deferred_strided_placements[p.dim].append((mesh_dim, p))

        else:
            ordered.append((mesh_dim, p))
            if isinstance(p, Shard):
                if p.dim in strided_part_ended_for_dim:
                    raise NotImplementedError(
                        f"Strided sharding does not allow Shard() to appear after "
                        f"the strided part has ended. {p} at mesh dim {mesh_dim} in "
                        f"{placements} violates this assumption."
                    )

                if p.dim in deferred_strided_placements:
                    strided_part_ended_for_dim.add(p.dim)
                    strided_placements = deferred_strided_placements.pop(p.dim)
                    aggregate_size = mesh_shape[mesh_dim]
                    while len(strided_placements) > 0:
                        strided_mesh_dim, strided = strided_placements.pop()
                        if not strided.split_factor == aggregate_size:
                            raise RuntimeError(
                                f"Can only convert _StridedShard to ordered Shard if split_factor({strided.split_factor})"
                                f" == aggregate mesh size ({aggregate_size})"
                            )
                        aggregate_size *= mesh_shape[strided_mesh_dim]
                        ordered.append((strided_mesh_dim, Shard(p.dim)))

    return ordered
