def _convert_helper(x, *, to_dtype):
  # Helper function for dtype conversion
  from_dtype = x.dtype
  if jnp.issubdtype(from_dtype, jnp.dtype("bool")):
    x = x.astype(jnp.int32)
    return _convert_helper(x, to_dtype=to_dtype)
  if jnp.issubdtype(from_dtype, jnp.integer):
    if from_dtype.itemsize < 4:
      x = x.astype(jnp.int32)
    if jnp.issubdtype(to_dtype, jnp.floating) and to_dtype.itemsize < 4:
      x = x.astype(jnp.float32)
    return x.astype(to_dtype)
  if jnp.issubdtype(from_dtype, jnp.floating):
    if jnp.issubdtype(to_dtype, jnp.integer):
      if from_dtype.itemsize < 4:
        x = x.astype(jnp.float32)
      if to_dtype.itemsize < 4:
        # Need to clip values to match XLA
        minval, maxval = jnp.iinfo(to_dtype).min, jnp.iinfo(to_dtype).max
        x = jnp.clip(x, minval, maxval)
        return x.astype(jnp.int32).astype(to_dtype)
      return x.astype(to_dtype)
    elif jnp.issubdtype(to_dtype, np.dtype("bool")):
      x = x.astype(jnp.int32)
    return x.astype(jnp.float32)
  raise NotImplementedError(f"Unsupported cast: {from_dtype} -> {to_dtype}")
