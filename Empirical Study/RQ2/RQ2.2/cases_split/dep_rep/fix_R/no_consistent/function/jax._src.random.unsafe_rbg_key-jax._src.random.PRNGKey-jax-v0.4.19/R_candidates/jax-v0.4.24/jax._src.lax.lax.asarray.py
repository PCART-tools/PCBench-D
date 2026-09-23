def asarray(x: ArrayLike) -> Array:
  """Lightweight conversion of ArrayLike input to Array output."""
  if isinstance(x, Array):
    return x
  if isinstance(x, (np.ndarray, np.generic, bool, int, float, builtins.complex)):
    return _convert_element_type(x, weak_type=dtypes.is_weakly_typed(x))
  else:
    raise TypeError(f"asarray: expected ArrayLike, got {x} of type {type(x)}.")
