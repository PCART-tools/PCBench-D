def _transpose(a: Array, *args: Any) -> Array:
  """Returns a view of the array with axes transposed.

  Refer to :func:`jax.numpy.transpose` for full documentation.
  """
  if not args:
    axis = None
  elif len(args) == 1:
    axis = args[0] if args[0] is None else _ensure_index_tuple(args[0])
  else:
    axis = _ensure_index_tuple(args)
  return transpose(a, axis)
