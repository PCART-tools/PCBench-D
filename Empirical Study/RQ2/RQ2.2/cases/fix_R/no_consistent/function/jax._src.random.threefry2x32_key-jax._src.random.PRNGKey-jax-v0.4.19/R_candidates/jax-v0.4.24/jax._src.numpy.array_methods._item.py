def _item(a: Array, *args) -> bool | int | float | complex:
  """Copy an element of an array to a standard Python scalar and return it."""
  arr = core.concrete_or_error(np.asarray, a, context="This occurred in the item() method of jax.Array")
  if dtypes.issubdtype(a.dtype, dtypes.extended):
    raise TypeError(f"No Python scalar type for {a.dtype=}")
  return arr.item(*args)
