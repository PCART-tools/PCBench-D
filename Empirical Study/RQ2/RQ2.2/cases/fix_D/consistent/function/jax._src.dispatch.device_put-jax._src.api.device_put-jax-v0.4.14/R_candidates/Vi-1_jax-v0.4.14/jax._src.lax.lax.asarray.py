def asarray(x: ArrayLike) -> Array:
  """Lightweight conversion of ArrayLike input to Array output."""
  if isinstance(x, Array):
    return x
  if isinstance(x, np.ndarray) or np.isscalar(x):
    # Call device_put_impl directly to avoid binding the primitive.
    return dispatch._device_put_impl(x)
  else:
    raise TypeError(f"asarray: expected ArrayLike, got {x} of type {type(x)}.")
