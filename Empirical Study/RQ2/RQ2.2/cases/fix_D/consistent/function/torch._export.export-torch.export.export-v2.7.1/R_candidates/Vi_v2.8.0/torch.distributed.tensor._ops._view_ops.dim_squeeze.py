def dim_squeeze(shape: Shape, dim: Optional[int] = None) -> DimMap:
    # FIXME: this is wrong when dim=None and one of the dimensions
    # equals size of the mesh. For example squeeze(DTensor(tensor(4), Shard[0])) could
    # end up as squeeze(tensor(1)) if we have 4 devices; this would lead to
    # removal of a dimension that is not actually a singleton.
    return tuple(
        InputDim(i)
        for i, s in enumerate(shape)
        if s > 1 or (dim is not None and i != normalize_dim(dim, len(shape)))
    )
