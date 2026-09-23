def _shaped_abstractify_slow(x):
  try:
    return core.raise_to_shaped(
      x if isinstance(x, core.AbstractValue) else core.get_aval(x))
  except TypeError:
    pass

  weak_type = getattr(x, 'weak_type', False)
  named_shape = getattr(x, 'named_shape', {})
  if hasattr(x, 'dtype'):
    dtype = dtypes.canonicalize_dtype(x.dtype, allow_extended_dtype=True)
  else:
    raise TypeError(
        f"Cannot interpret value of type {type(x)} as an abstract array; it "
        "does not have a dtype attribute")
  return core.ShapedArray(np.shape(x), dtype, weak_type=weak_type,
                          named_shape=named_shape)
