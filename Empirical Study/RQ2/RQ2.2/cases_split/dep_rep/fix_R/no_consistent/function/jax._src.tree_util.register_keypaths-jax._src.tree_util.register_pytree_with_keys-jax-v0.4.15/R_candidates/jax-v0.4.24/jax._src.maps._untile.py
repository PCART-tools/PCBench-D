def _untile(x, out_axes, axis_sizes):
  tile_shape = list(x.shape)
  shape = list(tile_shape)
  for name, axis in out_axes.items():
    shape[axis] *= axis_sizes[name]
  base_idxs = _tile_base_indices(tile_shape, out_axes, axis_sizes)

  padded = lax.broadcast(np.array(0, x.dtype), shape)
  padded = lax.dynamic_update_slice(padded, x, base_idxs)
  out = lax.psum(padded, tuple(out_axes.keys()))
  return out
