def shape_as_value(shape: core.Shape):
  """Converts a shape that may contain Poly values into a JAX value."""
  if len(shape) == 0:
    return full((0,), np.array(0, np.int64))
  dims = [
      expand_dims(convert_element_type(core.dimension_as_value(d), np.int64),
                  (0,))
      for d in shape
  ]
  return concatenate(dims, dimension=0)
