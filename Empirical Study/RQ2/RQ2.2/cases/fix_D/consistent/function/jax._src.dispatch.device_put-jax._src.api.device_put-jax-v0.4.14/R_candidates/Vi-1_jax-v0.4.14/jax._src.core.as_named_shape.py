def as_named_shape(shape) -> NamedShape:
  if isinstance(shape, NamedShape):
    return shape
  return NamedShape(*shape)
