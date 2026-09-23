def mesh_sharding_specs(axis_sizes, axis_names, allow_uneven_axes=False):
  mesh_axis_pos = {name: i for i, name in enumerate(axis_names)}
  # NOTE: This takes in the non-sharded avals!
  def mk_sharding_spec(aval, aval_axes):
    if aval is core.abstract_token:
      assert not aval_axes
      return ShardingSpec([], [Replicated(axis_size) for axis_size in axis_sizes.values()])
    aval_shape = list(aval.shape)
    # NOTE: sorted is stable, which is important when multiple resources
    #       map to the same axis.
    for name, axis in sorted(aval_axes.items(), key=lambda x: x[1]):
      if not allow_uneven_axes:
        if aval_shape[axis] % axis_sizes[name] != 0:
          raise ValueError(
            f'The aval shape on dimension {axis} is {aval_shape[axis]} and '
            f'the size of axis {name} is {axis_sizes[name]}. The aval shape % '
            'axis size should be zero but got '
            f'{aval_shape[axis] % axis_sizes[name]}')
      aval_shape[axis] //= axis_sizes[name]
    return sharding_specs.make_sharding_spec(
        axis_sizes, mesh_axis_pos, len(aval.shape), aval_axes)
  return mk_sharding_spec
