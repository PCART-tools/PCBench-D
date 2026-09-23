def propagate_shape_and_sharding(
    input_src_placements: Sequence[Placement],
    global_input_shape: Shape,
    rule: DimMap,
    mesh_sizes: Shape,
    strict_view: bool = False,
) -> tuple[Sequence[Placement], Sequence[Placement]]:
    """
    Determine input target sharding and output sharding based on
    given global tensor shape and input source sharding.

    Sharding propagation follows mapped dimensions:
    - An output dimension that maps directly to an input dimension is sharded equally
    - An output dimension that is a flattened set of input dimensions can only be
      sharded if only the leftmost flattened dimension is sharded.
    - An output dimension that is a split of the input dimension can only be sharded
      if the leftmost split size is divisible by the mesh dimension
    """
    assert len(input_src_placements) == len(mesh_sizes)
    # for each input dim, for each mesh dim, provides a list of possible shardable dimensions
    mesh_ndim = len(mesh_sizes)
    shardable_dims: dict[int, list[bool]] = {}

    # in case an input dimension disappears (e.g. collapsing, reduction)
    # we cannot shard in that dimension (we need a replication fall-back rule)
    seen_input_dims: set[int] = set()

    def collect_used_inputs(cmd: DimSpec) -> None:
        if isinstance(cmd, InputDim):
            seen_input_dims.add(cmd.input_dim)
        for inp in cmd.inputs():
            collect_used_inputs(inp)

    for cmd in rule:
        collect_used_inputs(cmd)
    for dim in range(len(global_input_shape)):
        shardable_dims[dim] = [dim in seen_input_dims] * mesh_ndim

    def maybe_get_shard_mesh_dim_and_placement(
        input_dim: InputDim,
    ) -> tuple[Optional[int], Optional[Shard]]:
        # if input_dim is sharded, return the mesh_dim and shard placement
        for i, placement in enumerate(input_src_placements):
            if isinstance(placement, Shard) and placement.dim == input_dim.input_dim:
                return i, placement
        return None, None

    def get_in_dim_to_shard(cmd: DimSpec) -> Optional[InputDim]:
        # TODO(whc) this helper is pretty hard to understand, at least it should be better documented if not refactored
        if isinstance(cmd, InputDim):
            return cmd
        elif isinstance(cmd, Flatten):
            for i, dim in enumerate(cmd.input_dims):
                if isinstance(dim, InputDim):
                    can_shard_dim = True
                    shard_mesh_dim, shard_placement = (
                        maybe_get_shard_mesh_dim_and_placement(dim)
                    )
                    input_sharded = shard_mesh_dim is not None
                    if i > 0:
                        can_shard_dim = False
                        if strict_view and input_sharded:
                            raise RuntimeError(
                                f"Attempted to flatten sharded dimension {i}, ",
                                "but only the leftmost dim of a Flatten can be sharded.",
                            )
                    elif input_sharded:
                        assert (
                            shard_placement is not None and shard_mesh_dim is not None
                        )
                        tensor_dim_size = global_input_shape[shard_placement.dim]
                        mesh_dim_size = mesh_sizes[shard_mesh_dim]
                        if tensor_dim_size % mesh_dim_size != 0:
                            can_shard_dim = False
                            if strict_view:
                                raise RuntimeError(
                                    f"Attempted to flatten unevenly sharded dimension {i}, "
                                    "which would require resharding the input. "
                                    "Please explicitly redistribute the tensor instead."
                                )

                    shardable_dims[dim.input_dim] = [can_shard_dim] * mesh_ndim
            dim0 = cmd.input_dims[0]
            # TODO(whc) dim0 can be sharded or not sharded, can't it?
            # should we only return it if its sharded in the placement?
            return dim0 if isinstance(dim0, InputDim) else None
        elif isinstance(cmd, Split):
            in_dim = get_in_dim_to_shard(cmd.input_dim)
            out_size = cmd.group_shape[cmd.split_id]
            if cmd.split_id == 0 and in_dim is not None:
                # we need to check that the input dimension is divisible
                # by the size of the submesh we're sharding it on
                # NOTE: it would be possible to shard the same input dimension
                # on more than one mesh dimension. In that case, the dimension
                # needs to be divisible by the product of mesh sizes.
                # In order to keep the problem more tractable, we will not consider
                # double resharding as a suggestion (e.g. [Shard(0), Shard(0) ])
                # but we will allow it if that's the input and it's compatible

                # 1. is this dimension shardable on each individual mesh dim?
                shardable_dims[in_dim.input_dim] = [
                    out_size % mesh_dim_size == 0 for mesh_dim_size in mesh_sizes
                ]

                # 2. here we special case things like [Shard(0), Shard(0)]
                submesh_size = 1
                for size, shard in zip(mesh_sizes, input_src_placements):
                    if isinstance(shard, Shard) and shard.dim == in_dim:
                        submesh_size *= size
                assert out_size % submesh_size == 0, (
                    f"Resulting dimension size {out_size} is not divisible by its mesh dimension {submesh_size}."
                )

            # we will only shard our first component of the split
            return in_dim if cmd.split_id == 0 else None
        elif isinstance(cmd, Repeat):
            in_dim = get_in_dim_to_shard(cmd.input_dim)
            if in_dim is not None:
                shardable_dims[in_dim.input_dim] = [False] * mesh_ndim
            return None
        else:
            return None

    # for each output dim, find the corresponding input dim in terms of sharding prop
    shard_dim_map = {}
    for dim, cmd in enumerate(rule):
        in_dim = get_in_dim_to_shard(cmd)
        if in_dim is not None:
            shard_dim_map[in_dim.input_dim] = dim

    input_tgt_placements = [
        (
            Replicate()
            if isinstance(p, Shard) and not shardable_dims[p.dim][mesh_dim]
            else p
        )
        for mesh_dim, p in enumerate(input_src_placements)
    ]
    output_placements = [
        Shard(shard_dim_map[p.dim]) if isinstance(p, Shard) else p
        for p in input_tgt_placements
    ]

    return input_tgt_placements, output_placements
