def threefry_seed(seed: int) -> jnp.ndarray:
  """Create a single raw threefry PRNG key given an integer seed.

  Args:
    seed: a 64- or 32-bit integer used as the value of the key.

  Returns:
    The PRNG key contents, modeled as an array of shape (2,) and dtype
    uint32. The key is constructed from a 64-bit seed by effectively
    bit-casting to a pair of uint32 values (or from a 32-bit seed by
    first padding out with zeros).
  """
  # Avoid overflowerror in X32 mode by first converting ints to int64.
  # This breaks JIT invariance for large ints, but supports the common
  # use-case of instantiating with Python hashes in X32 mode.
  if isinstance(seed, int):
    seed_arr = jnp.asarray(np.int64(seed))
  else:
    seed_arr = jnp.asarray(seed)
  if seed_arr.shape:
    raise TypeError(f"PRNG key seed must be a scalar; got {seed!r}.")
  if not np.issubdtype(seed_arr.dtype, np.integer):
    raise TypeError(f"PRNG key seed must be an integer; got {seed!r}")
  convert = lambda k: lax.reshape(lax.convert_element_type(k, np.uint32), [1])
  k1 = convert(
      lax.shift_right_logical(seed_arr, lax_internal._const(seed_arr, 32)))
  with jax.numpy_dtype_promotion('standard'):
    # TODO(jakevdp): in X64 mode, this can generate 64-bit computations for 32-bit
    # inputs. We should avoid this.
    k2 = convert(jnp.bitwise_and(seed_arr, np.uint32(0xFFFFFFFF)))
  return lax.concatenate([k1, k2], 0)
