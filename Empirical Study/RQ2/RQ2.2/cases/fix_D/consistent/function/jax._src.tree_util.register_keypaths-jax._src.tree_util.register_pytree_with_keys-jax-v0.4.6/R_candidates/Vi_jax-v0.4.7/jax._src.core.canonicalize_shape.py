def canonicalize_shape(shape: Shape, context: str="") -> Tuple[Any, ...]:
  """Canonicalizes and checks for errors in a user-provided shape value.

  Args:
    shape: a Python value that represents a shape.

  Returns:
    A tuple of canonical dimension values.
  """
  try:
    return tuple(unsafe_map(_canonicalize_dimension, shape))
  except TypeError:
    pass
  raise _invalid_shape_error(shape, context)
