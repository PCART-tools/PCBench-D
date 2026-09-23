def _rng_bit_generator_weak_type_rule(key, *, shape, dtype, algorithm):
  del shape, dtype, algorithm
  return (key.weak_type, False)
