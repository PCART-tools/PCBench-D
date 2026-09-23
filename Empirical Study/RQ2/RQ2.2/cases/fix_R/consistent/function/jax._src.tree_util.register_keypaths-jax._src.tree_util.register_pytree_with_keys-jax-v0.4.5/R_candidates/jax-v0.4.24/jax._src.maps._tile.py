def _tile(x, in_axes, axis_sizes):
  if not in_axes:
    return x
  tile_shape = list(x.shape)
  for name, axis in in_axes.items():
    axis_size = axis_sizes[name]
    assert tile_shape[axis] % axis_size == 0
    tile_shape[axis] //= axis_size
  base_idxs = _tile_base_indices(tile_shape, in_axes, axis_sizes)
  return lax.dynamic_slice(x, base_idxs, tile_shape)
