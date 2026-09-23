def replicate_tensor_dim(
    placements: Sequence[Placement], dim: int
) -> tuple[Placement, ...]:
    """Force the given tensor dimension to be replicated."""
    # Not using p.is_shard() to avoid mypy complain about Placement not having
    # attribute dim.
    return tuple(
        Replicate() if p.is_partial() or isinstance(p, Shard) and p.dim == dim else p
        for p in placements
    )
