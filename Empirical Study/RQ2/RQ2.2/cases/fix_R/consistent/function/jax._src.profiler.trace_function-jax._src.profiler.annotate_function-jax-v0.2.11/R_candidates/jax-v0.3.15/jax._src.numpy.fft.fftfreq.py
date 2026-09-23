@_wraps(np.fft.fftfreq)
def fftfreq(n, d=1.0):
  dtype = dtypes.canonicalize_dtype(jnp.float_)
  if isinstance(n, (list, tuple)):
    raise ValueError(
          "The n argument of jax.numpy.fft.fftfreq only takes an int. "
          "Got n = %s." % list(n))

  elif isinstance(d, (list, tuple)):
    raise ValueError(
          "The d argument of jax.numpy.fft.fftfreq only takes a single value. "
          "Got d = %s." % list(d))

  k = jnp.zeros(n, dtype=dtype)
  if n % 2 == 0:
    # k[0: n // 2 - 1] = jnp.arange(0, n // 2 - 1)
    k = k.at[0: n // 2].set( jnp.arange(0, n // 2, dtype=dtype))

    # k[n // 2:] = jnp.arange(-n // 2, -1)
    k = k.at[n // 2:].set( jnp.arange(-n // 2, 0, dtype=dtype))

  else:
    # k[0: (n - 1) // 2] = jnp.arange(0, (n - 1) // 2)
    k = k.at[0: (n - 1) // 2 + 1].set(jnp.arange(0, (n - 1) // 2 + 1, dtype=dtype))

    # k[(n - 1) // 2 + 1:] = jnp.arange(-(n - 1) // 2, -1)
    k = k.at[(n - 1) // 2 + 1:].set(jnp.arange(-(n - 1) // 2, 0, dtype=dtype))

  return k / (d * n)
