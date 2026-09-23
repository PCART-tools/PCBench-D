@_wraps(np.fft.rfftfreq)
def rfftfreq(n, d=1.0):
  dtype = dtypes.canonicalize_dtype(jnp.float_)
  if isinstance(n, (list, tuple)):
    raise ValueError(
          "The n argument of jax.numpy.fft.rfftfreq only takes an int. "
          "Got n = %s." % list(n))

  elif isinstance(d, (list, tuple)):
    raise ValueError(
          "The d argument of jax.numpy.fft.rfftfreq only takes a single value. "
          "Got d = %s." % list(d))

  if n % 2 == 0:
    k = jnp.arange(0, n // 2 + 1, dtype=dtype)

  else:
    k = jnp.arange(0, (n - 1) // 2 + 1, dtype=dtype)

  return k / (d * n)
