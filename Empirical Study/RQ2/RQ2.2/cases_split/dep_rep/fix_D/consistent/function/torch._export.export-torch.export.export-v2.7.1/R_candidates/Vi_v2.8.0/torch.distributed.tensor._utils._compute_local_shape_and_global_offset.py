def _compute_local_shape_and_global_offset(
    global_shape: ShapeType,
    mesh_shape: ShapeType,
    my_coordinate: Optional[list[int]],
    placements: Sequence[Placement],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    ordered_placements = _explicit_order_placements(mesh_shape, placements)

    if my_coordinate is None:
        # if rank not in the mesh, return empty offset
        return ((0,), ())
    else:
        local_shape = list(global_shape)
        global_offset = [0] * len(global_shape)
        for mesh_dim, placement in ordered_placements:
            mesh_dim_size = mesh_shape[mesh_dim]
            if isinstance(placement, Shard):
                shard_dim = placement.dim
                local_offset = [0] * len(global_shape)
                assert shard_dim < len(local_shape), (
                    f"Sharding dim {shard_dim} greater than tensor ndim {len(local_shape)}"
                )
                shard_size, shard_offset = placement._local_shard_size_and_offset(
                    local_shape[shard_dim],
                    mesh_dim_size,
                    my_coordinate[mesh_dim],
                )

                local_shape[shard_dim] = shard_size
                local_offset[shard_dim] = shard_offset
                if shard_size == 0:
                    # Special case to fill in a standardized non-garbage value for the global_offset
                    # of zero-sized shards.  This value is out of bounds of the tensor, so it won't conflict
                    # with any real offsets.  DCP may rely on this value to de-duplicate shards.
                    global_offset[shard_dim] = global_shape[shard_dim]
                else:
                    # On a given dimension, if the local_offset[shard_dim] is smaller than global_offset[shard_dim],
                    # it means that this dimension has been already sharded in previous placement.
                    # Therefore, we cannot simply replace the global_offset[shard_dim] with local_offset[shard_dim].
                    # Instead, for the given shard_dim, we need to add local_offset[shard_dim] to existing global_offset[shard_dim].
                    if global_offset[shard_dim] <= local_offset[shard_dim]:
                        global_offset[shard_dim] = local_offset[shard_dim]
                    else:
                        global_offset[shard_dim] += local_offset[shard_dim]

        # NOTE: the offset compute relies on the local shard index and it has no
        # problem when strided sharding is not present. To correctly compute, we assume
        # that the ``_StridedShard.split_factor`` field encodes how many partitions
        # each local tensor will be further split into when sharding on higher mesh
        # dimensions. However, this number is only correct if the DTensor is not
        # sharded after the strided sharding completes. For example,
        # [Shard(0), _StridedShard(0, split_factor=2), Shard(0)] is the placements
        # where the DTensor's dim-0 is first sharded on device mesh dim-0, then on
        # device mesh dim-2, and last on mesh dim-1. We define the
        # "_StridedShard(0, split_factor=2), Shard(0)" part as the strided sharding
        # part because strided sharding happens on mesh dim-1 and it was caused by
        # the fact that sharding on dim-2 occurred ahead. In this case, there's no
        # further sharding after this strided sharding part and ``split_factor``
        # correctly encodes the number. Another example is
        # [_StridedShard(0, split_factor=2), Shard(0), Shard(0)] where the DTensor's
        # dim-0 is first sharded on mesh dim-1, then on mesh dim-0, and last on mesh
        # dim-2. This violates our assumption that no further sharding shall occur
        # after the strided sharding part and ``split_factor`` won't correctly
        # encode the number of further split. So far, the only case where _StridedShard
        # placement would appear is FSDP2 + TP on 2D mesh and the above case could only
        # happen on mesh of 3 or more dimensions.
        # TODO: change this function to correctly address this.
        # TODO: this logic can be applied to contiguous sharding as well
        return tuple(local_shape), tuple(global_offset)
