def threefry_seed(seed: jax.Array) -> jax.Array:
  """Create a single raw threefry PRNG key from an integer seed.

  Args:
    seed: a 64- or 32-bit integer used as the value of the key.

  Returns:
    The PRNG key contents, modeled as an array of shape (2,) and dtype
    uint32. The key is constructed from a 64-bit seed by effectively
    bit-casting to a pair of uint32 values (or from a 32-bit seed by
    first padding out with zeros).
  """
  if seed.shape:
    raise TypeError(f"PRNG key seed must be a scalar; got {seed!r}.")
  if not np.issubdtype(seed.dtype, np.integer):
    raise TypeError(f"PRNG key seed must be an integer; got {seed!r}")
  convert = lambda k: lax.reshape(lax.convert_element_type(k, np.uint32), [1])
  k1 = convert(
      lax.shift_right_logical(seed, lax_internal._const(seed, 32)))
  with jax.numpy_dtype_promotion('standard'):
    # TODO(jakevdp): in X64 mode, this can generate 64-bit computations for 32-bit
    # inputs. We should avoid this.
    k2 = convert(jnp.bitwise_and(seed, np.uint32(0xFFFFFFFF)))
  return lax.concatenate([k1, k2], 0)
