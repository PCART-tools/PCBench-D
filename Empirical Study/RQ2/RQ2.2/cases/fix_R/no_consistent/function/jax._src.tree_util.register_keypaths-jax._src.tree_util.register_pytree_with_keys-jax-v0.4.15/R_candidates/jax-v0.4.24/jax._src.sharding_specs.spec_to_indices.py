def spec_to_indices(shape: Sequence[int],
                    spec: ShardingSpec) -> tuple[Index, ...]:
  """Returns numpy-style indices corresponding to a sharding spec.

  Each index describes a shard of the array. The order of the indices is the
  same as the device_buffers of a Array sharded using PmapSharding (i.e. the
  data is laid out row-major).

  Args:
    shape: The shape of the logical array being sharded.
    spec: Describes how the array is sharded and how the shards are assigned to
      the logical mesh.

  Returns:
    A tuple of length equal to the size of the mesh (inferred as the product of
    sharded dimension sizes and all replication factors).  Each element is an
    int, a slice object with step=1, or a tuple thereof, to be treated as an
    index into the full logical array.
  """
  return tuple(spec.indices(shape).flat)  # type: ignore
