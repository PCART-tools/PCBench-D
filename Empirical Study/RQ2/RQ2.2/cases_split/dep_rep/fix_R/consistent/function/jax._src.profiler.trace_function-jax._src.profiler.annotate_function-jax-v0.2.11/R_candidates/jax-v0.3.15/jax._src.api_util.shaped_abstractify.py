def shaped_abstractify(x):
  try:
    return core.raise_to_shaped(
      x if isinstance(x, core.AbstractValue) else core.get_aval(x))
  except TypeError:
    pass

  weak_type = getattr(x, 'weak_type', False)
  named_shape = getattr(x, 'named_shape', {})
  return core.ShapedArray(np.shape(x), _dtype(x), weak_type=weak_type,
                          named_shape=named_shape)
