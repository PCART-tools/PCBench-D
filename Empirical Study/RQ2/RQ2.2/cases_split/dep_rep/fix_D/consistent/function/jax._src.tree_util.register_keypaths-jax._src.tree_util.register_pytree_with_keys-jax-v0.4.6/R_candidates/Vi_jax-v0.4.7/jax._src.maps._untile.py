def _untile(x, out_axes, axis_sizes, platform):
  # TODO(mattjj): remove this logic when AllReduce PRED supported on CPU / GPU
  convert_bool = (np.issubdtype(x.dtype, np.bool_)
                  and platform in ('cpu', 'gpu'))
  if convert_bool:
    x = lax.convert_element_type(x, np.dtype(np.float32))

  tile_shape = list(x.shape)
  shape = list(tile_shape)
  for name, axis in out_axes.items():
    shape[axis] *= axis_sizes[name]
  base_idxs = _tile_base_indices(tile_shape, out_axes, axis_sizes)

  padded = lax.broadcast(np.array(0, x.dtype), shape)
  padded = lax.dynamic_update_slice(padded, x, base_idxs)
  out = lax.psum(padded, tuple(out_axes.keys()))

  # TODO(mattjj): remove this logic when AllReduce PRED supported on CPU / GPU
  if convert_bool:
    nonzero = lax.ne(out, np.array(0, dtype=np.float32))
    out = lax.convert_element_type(nonzero, np.dtype(np.bool_))
  return out
