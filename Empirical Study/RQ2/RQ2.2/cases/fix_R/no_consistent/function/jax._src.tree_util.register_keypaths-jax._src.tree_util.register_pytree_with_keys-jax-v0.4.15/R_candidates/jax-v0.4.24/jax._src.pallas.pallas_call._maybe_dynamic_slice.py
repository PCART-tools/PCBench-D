def _maybe_dynamic_slice(start_idx, block_shape, value, is_indexing):
  if start_idx is None:
    assert is_indexing is None
    return value
  assert is_indexing is not None
  start_idx = tuple(jnp.asarray(s, dtype=jnp.int32) for s in start_idx)
  output = lax.dynamic_slice(value, start_idx, slice_sizes=block_shape)
  squeeze_dims = tuple(np.arange(len(is_indexing))[np.array(is_indexing,
                                                            dtype=np.bool_)])
  return lax.squeeze(output, squeeze_dims)
