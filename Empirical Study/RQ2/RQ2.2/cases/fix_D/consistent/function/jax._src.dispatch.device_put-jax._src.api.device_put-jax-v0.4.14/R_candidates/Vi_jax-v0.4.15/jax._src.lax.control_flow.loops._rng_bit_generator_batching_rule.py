def _rng_bit_generator_batching_rule(batched_args, batch_dims, *, shape, dtype, algorithm):
  """Calls RBG in a loop and stacks the results."""
  key, = batched_args
  bd, = batch_dims
  if bd is batching.not_mapped:
    return lax.rng_bit_generator_p.bind(key, shape=shape, dtype=dtype,
                                        algorithm=algorithm), (None, None)
  key = batching.moveaxis(key, bd, 0)
  map_body = lambda k: lax.rng_bit_generator_p.bind(k, shape=shape, dtype=dtype, algorithm=algorithm)
  stacked_keys, stacked_bits = map(map_body, key)
  return (stacked_keys, stacked_bits), (0, 0)
