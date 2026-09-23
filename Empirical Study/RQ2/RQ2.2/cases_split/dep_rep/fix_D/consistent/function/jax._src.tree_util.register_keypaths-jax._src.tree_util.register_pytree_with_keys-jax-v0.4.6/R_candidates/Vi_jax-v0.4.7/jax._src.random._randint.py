@partial(jit, static_argnums=(1, 4), inline=True)
def _randint(key, shape, minval, maxval, dtype) -> Array:
  _check_shape("randint", shape, np.shape(minval), np.shape(maxval))
  if not jnp.issubdtype(dtype, np.integer):
    raise TypeError(f"randint only accepts integer dtypes, got {dtype}")

  check_arraylike("randint", minval, maxval)
  minval = jnp.asarray(minval)
  maxval = jnp.asarray(maxval)
  if not jnp.issubdtype(minval.dtype, np.integer):
    minval = minval.astype(int)
  if not jnp.issubdtype(maxval.dtype, np.integer):
    maxval = maxval.astype(int)

  # Flag where maxval is greater than the maximum value of dtype
  # in order to handle cases like randint(key, shape, 0, 256, 'uint8')
  maxval_out_of_range = lax.gt(
    maxval, _convert_and_clip_integer(jnp.array(jnp.iinfo(dtype).max, dtype), maxval.dtype))

  minval = _convert_and_clip_integer(minval, dtype)
  maxval = _convert_and_clip_integer(maxval, dtype)
  minval = lax.broadcast_to_rank(minval, len(shape))
  maxval = lax.broadcast_to_rank(maxval, len(shape))
  nbits = jnp.iinfo(dtype).bits

  if nbits not in (8, 16, 32, 64):
    raise TypeError(f"randint only accepts 8-, 16-, 32-, or 64-bit dtypes, got {dtype}")

  # This algorithm is biased whenever (maxval - minval) is not a power of 2.
  # We generate double the number of random bits required by the dtype so as to
  # reduce that bias.
  k1, k2 = _split(key)
  rbits = lambda key: _random_bits(key, nbits, shape)
  higher_bits, lower_bits = rbits(k1), rbits(k2)

  unsigned_dtype = UINT_DTYPES[nbits]
  span = lax.convert_element_type(maxval - minval, unsigned_dtype)

  # Ensure that span=1 when maxval <= minval, so minval is always returned;
  # https://github.com/google/jax/issues/222
  span = lax.select(maxval <= minval, lax.full_like(span, 1), span)

  # When maxval is out of range, the span has to be one larger.
  # If span is already the maximum representable value, this will wrap to zero,
  # causing remainders below to have no effect, which is the correct semantics.
  span = lax.select(
    maxval_out_of_range & (maxval > minval),
    lax.add(span, _lax_const(span, 1)),
    span)

  # To compute a remainder operation on an integer that might have twice as many
  # bits as we can represent in the native unsigned dtype, we compute a
  # multiplier equal to 2**nbits % span. To avoid overflow, we use the identity:
  #  (a * b) % N = [(a % N) * (b % N)] % N
  multiplier = lax.rem(_lax_const(span, 2 ** (nbits // 2)), span)
  multiplier = lax.rem(lax.mul(multiplier, multiplier), span)

  random_offset = lax.add(lax.mul(lax.rem(higher_bits, span), multiplier),
                          lax.rem(lower_bits, span))
  random_offset = lax.rem(random_offset, span)
  return lax.add(minval, lax.convert_element_type(random_offset, dtype))
