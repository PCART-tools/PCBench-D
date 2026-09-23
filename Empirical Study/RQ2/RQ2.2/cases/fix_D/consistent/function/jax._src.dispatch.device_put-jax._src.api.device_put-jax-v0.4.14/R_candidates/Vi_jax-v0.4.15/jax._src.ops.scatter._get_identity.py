def _get_identity(op, dtype):
  """Get an appropriate identity for a given operation in a given dtype."""
  if op is lax.scatter_add:
    return 0
  elif op is lax.scatter_mul:
    return 1
  elif op is lax.scatter_min:
    if dtype == dtypes.bool_:
      return True
    elif jnp.issubdtype(dtype, jnp.integer):
      return jnp.iinfo(dtype).max
    return float('inf')
  elif op is lax.scatter_max:
    if dtype == dtypes.bool_:
      return False
    elif jnp.issubdtype(dtype, jnp.integer):
      return jnp.iinfo(dtype).min
    return -float('inf')
  else:
    raise ValueError(f"Unrecognized op: {op}")
