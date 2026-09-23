def rand_bool(rng):
  def generator(shape, dtype):
    return _cast_to_shape(rng.rand(*_dims_of_shape(shape)) < 0.5, shape, dtype)
  return generator
