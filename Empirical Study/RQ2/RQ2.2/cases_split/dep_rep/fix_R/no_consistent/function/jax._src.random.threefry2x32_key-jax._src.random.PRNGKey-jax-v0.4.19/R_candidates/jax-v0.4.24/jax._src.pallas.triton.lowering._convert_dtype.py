def _convert_dtype(dtype: jnp.dtype) -> tc.dtype:
  if dtype == jnp.float32:
    return tc.float32
  elif dtype == jnp.float64:
    return tc.float64
  elif dtype == jnp.float16:
    return tc.float16
  elif dtype == jnp.bfloat16:
    return tc.bfloat16
  elif dtype == jnp.uint32:
    return tc.uint32
  elif dtype == jnp.uint64:
    return tc.uint64
  elif dtype == jnp.int32:
    return tc.int32
  elif dtype == jnp.int64:
    return tc.int64
  elif dtype == jnp.bool_:
    return tc.int1
  raise ValueError(f"Unhandled dtype: {dtype}")
