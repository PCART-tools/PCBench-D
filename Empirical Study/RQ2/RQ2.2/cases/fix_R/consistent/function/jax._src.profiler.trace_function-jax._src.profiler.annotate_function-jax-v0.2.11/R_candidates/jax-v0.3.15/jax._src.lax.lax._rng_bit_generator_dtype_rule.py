def _rng_bit_generator_dtype_rule(key, *, shape, dtype, algorithm):
  del shape, algorithm
  return (key.dtype, dtype)
