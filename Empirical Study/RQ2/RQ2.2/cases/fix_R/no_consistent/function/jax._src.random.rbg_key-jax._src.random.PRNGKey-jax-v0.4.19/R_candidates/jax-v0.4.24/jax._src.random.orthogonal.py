def orthogonal(
  key: KeyArrayLike,
  n: int,
  shape: Shape = (),
  dtype: DTypeLikeFloat = float
) -> Array:
  """Sample uniformly from the orthogonal group O(n).

  If the dtype is complex, sample uniformly from the unitary group U(n).

  Args:
    key: a PRNG key used as the random key.
    n: an integer indicating the resulting dimension.
    shape: optional, the batch dimensions of the result. Default ().
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).

  Returns:
    A random array of shape `(*shape, n, n)` and specified dtype.
  """
  key, _ = _check_prng_key("orthogonal", key)
  dtypes.check_user_dtype_supported(dtype)
  _check_shape("orthogonal", shape)
  n = core.concrete_or_error(index, n, "The error occurred in jax.random.orthogonal()")
  z = normal(key, (*shape, n, n), dtype)
  q, r = jnp.linalg.qr(z)
  d = jnp.diagonal(r, 0, -2, -1)
  return lax.mul(q, lax.expand_dims(lax.div(d, abs(d).astype(d.dtype)), [-2]))
