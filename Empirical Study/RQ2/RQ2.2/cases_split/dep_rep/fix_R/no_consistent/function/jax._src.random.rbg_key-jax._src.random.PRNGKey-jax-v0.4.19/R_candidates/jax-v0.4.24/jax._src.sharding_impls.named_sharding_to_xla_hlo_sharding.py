@functools.lru_cache(maxsize=4096)
def named_sharding_to_xla_hlo_sharding(
    self, num_dimensions: int) -> xc.HloSharding:
  mesh_shape = self.mesh.shape
  array_mapping = get_array_mapping(self._parsed_pspec)
  mesh_axis_pos = {name: i for i, name in enumerate(self.mesh.axis_names)}

  special_axes = {}
  if self._manual_axes:
    axis_names = self.mesh.axis_names
    for manual_axis in self._manual_axes:
      special_axes[axis_names.index(manual_axis)] = xc.OpSharding.Type.MANUAL

  replicated_mesh_axes = []
  for i, (axis_name, axis_val) in enumerate(mesh_shape.items()):
    if axis_name not in array_mapping:  # type: ignore
      replicated_mesh_axes.append((i, axis_val))

  if len(replicated_mesh_axes) == len(mesh_shape) and not special_axes:
    return xc.HloSharding.replicate()

  mesh_permutation = []
  new_mesh_shape = [1] * num_dimensions
  for name, pos in sorted(array_mapping.items(), key=lambda x: x[1]):  # type: ignore
    new_mesh_shape[pos] *= mesh_shape[name]
    mesh_permutation.append(mesh_axis_pos[name])

  last_tile_dims = []
  if replicated_mesh_axes:
    axes_by_type = collections.defaultdict(list)
    size_by_type = collections.defaultdict(lambda: 1)  # type: ignore
    assert {x[0] for x in replicated_mesh_axes}.issuperset(set(special_axes.keys()))
    for i, size in replicated_mesh_axes:
      ty = special_axes.get(i, xc.OpSharding.Type.REPLICATED)
      axes_by_type[ty].append(i)
      size_by_type[ty] *= size
    for ty, axes in sorted(axes_by_type.items(), key=lambda x: x[0].value):
      last_tile_dims.append(ty)
      new_mesh_shape.append(size_by_type[ty])
      mesh_permutation.extend(axes)

  # Explanation of the parameters of `HloSharding.iota_tile`.
  # This is the HloShardingV2 format:
  #   * dims: How many ways each dimension is sharded.
  #       Replicated/Manual dims are added added at the end
  #   * reshape_dims: This is the just the shape of the mesh.
  #   * transpose_perm: This is the order in which mesh axes in PartitionSpec
  #       appear relative to mesh.axis_names order.
  #   * subgroup_types: List of type of OpSharding. Type can be REPLICATED and MANUAL.
  # Let's see an example:
  #   Consider input_shape=(8, 4, 2, 2), mesh={'a': 2, 'b': 2, 'c': 2, 'd': 2}
  #   and partition_spec=P(None, ('d', 'b'), 'c').
  #   Arguments to iota_tile will be:
  #     dims = [1, 4, 2, 1, 2]  # 'a' is replicated hence `2` is at the end.
  #     reshape_dims = [2, 2, 2, 2]
  #     transpose_perm = [3, 1, 2, 0]  # 'a' is replicated hence 0 is at the end
  #     subgroup_types = [xc.OpSharding.Type.REPLICATED]
  return xc.HloSharding.iota_tile(
      dims=new_mesh_shape, reshape_dims=tuple(self.mesh.shape.values()),
      transpose_perm=mesh_permutation, subgroup_types=last_tile_dims)
