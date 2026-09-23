def rng_bit_generator(key, shape, dtype=np.uint32,
                      algorithm=RandomAlgorithm.RNG_DEFAULT):
  """Stateless PRNG bit generator. Experimental and its use is discouraged.

  Returns uniformly distributed random bits with the specified shape and dtype
  (what is required to be an integer type) using the platform specific
  default algorithm or the one specified.

  It provides direct access to the RngBitGenerator primitive exposed by XLA
  (https://www.tensorflow.org/xla/operation_semantics#rngbitgenerator) for low
  level API access.

  Most users should use `jax.random` instead for a stable and more user
  friendly API.
  """
  shape = core.canonicalize_shape(shape)
  dtype = dtypes.canonicalize_dtype(dtype)
  if np.dtype(dtype) not in {np.dtype('uint8'), np.dtype('uint16'),
                             np.dtype('uint32'), np.dtype('uint64')}:
    raise TypeError(f'rng_bit_generator: unsupported dtype {dtype}')
  return tuple(
      rng_bit_generator_p.bind(
          key, shape=shape, dtype=dtype, algorithm=algorithm))
