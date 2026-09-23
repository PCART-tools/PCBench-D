def normalize_shard_for_stack(
    placements: Sequence[Placement], insert_dim: int = 0
) -> Sequence[Placement]:
    # stack op would "insert" new dim, so all sharded dim >= the inserted dim need to
    # be normalized with the new Shard placement
    normalized_placements: list[Placement] = []
    for placement in placements:
        if isinstance(placement, Shard) and placement.dim >= insert_dim:
            normalized_placements.append(Shard(placement.dim + 1))
        else:
            normalized_placements.append(placement)
    return normalized_placements
