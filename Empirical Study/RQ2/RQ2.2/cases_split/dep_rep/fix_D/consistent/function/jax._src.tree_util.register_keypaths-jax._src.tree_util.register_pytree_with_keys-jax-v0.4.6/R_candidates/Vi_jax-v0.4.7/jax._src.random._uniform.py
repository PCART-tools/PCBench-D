@partial(jit, static_argnums=(1, 2), inline=True)
def _uniform(key, shape, dtype, minval, maxval) -> Array:
  _check_shape("uniform", shape)
  if not jnp.issubdtype(dtype, np.floating):
    raise TypeError("uniform only accepts floating point dtypes.")

  minval = lax.convert_element_type(minval, dtype)
  maxval = lax.convert_element_type(maxval, dtype)
  minval = lax.broadcast_to_rank(minval, shape.positional_rank)
  maxval = lax.broadcast_to_rank(maxval, shape.positional_rank)

  finfo = jnp.finfo(dtype)
  nbits, nmant = finfo.bits, finfo.nmant

  if nbits not in (16, 32, 64):
    raise TypeError("uniform only accepts 32- or 64-bit dtypes.")

  rng_bits = nbits
  if xla_extension_version >= 140 and nmant < 8:
    rng_bits = 8
  bits = _random_bits(key, rng_bits, shape)
  uint_dtype = UINT_DTYPES[nbits]
  if rng_bits != nbits:
    bits = lax.convert_element_type(bits, uint_dtype)

  # The strategy here is to randomize only the mantissa bits with an exponent of
  # 1 (after applying the bias), then shift and scale to the desired range. The
  # bit-level transformation we use relies on Numpy and XLA having bit-for-bit
  # equivalent float representations, which might not be true on all platforms.
  float_bits = lax.bitwise_or(
      lax.shift_right_logical(bits, np.array(rng_bits - nmant, uint_dtype)),
      np.array(1.0, dtype).view(uint_dtype),
  )
  floats = lax.bitcast_convert_type(float_bits, dtype) - np.array(1., dtype)
  return lax.max(
      minval,
      lax.reshape(floats * (maxval - minval) + minval, shape.positional))
