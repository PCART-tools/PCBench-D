def fftfreq(n: int, d: ArrayLike = 1.0, *, dtype: DTypeLike | None = None,
            device: xla_client.Device | Sharding | None = None) -> Array:
  """Return sample frequencies for the discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.fftfreq`. Returns frequencies appropriate
  for use with the outputs of :func:`~jax.numpy.fft.fft` and :func:`~jax.numpy.fft.ifft`.

  Args:
    n: length of the FFT window
    d: optional scalar sample spacing (default: 1.0)
    dtype: optional dtype of returned frequencies. If not specified, JAX's default
      floating point dtype will be used.
    device: optional :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of sample frequencies, length ``n``.

  See also:
    - :func:`jax.numpy.fft.rfftfreq`: frequencies for use with
      :func:`~jax.numpy.fft.rfft` and :func:`~jax.numpy.fft.irfft`.
  """
  dtype = dtype or dtypes.canonicalize_dtype(jnp.float_)
  if isinstance(n, (list, tuple)):
    raise ValueError(
          "The n argument of jax.numpy.fft.fftfreq only takes an int. "
          "Got n = %s." % list(n))

  elif isinstance(d, (list, tuple)):
    raise ValueError(
          "The d argument of jax.numpy.fft.fftfreq only takes a single value. "
          "Got d = %s." % list(d))

  k = jnp.zeros(n, dtype=dtype, device=device)
  if n % 2 == 0:
    # k[0: n // 2 - 1] = jnp.arange(0, n // 2 - 1)
    k = k.at[0: n // 2].set(jnp.arange(0, n // 2, dtype=dtype))

    # k[n // 2:] = jnp.arange(-n // 2, -1)
    k = k.at[n // 2:].set(jnp.arange(-n // 2, 0, dtype=dtype))

  else:
    # k[0: (n - 1) // 2] = jnp.arange(0, (n - 1) // 2)
    k = k.at[0: (n - 1) // 2 + 1].set(jnp.arange(0, (n - 1) // 2 + 1, dtype=dtype))

    # k[(n - 1) // 2 + 1:] = jnp.arange(-(n - 1) // 2, -1)
    k = k.at[(n - 1) // 2 + 1:].set(jnp.arange(-(n - 1) // 2, 0, dtype=dtype))

  return k / jnp.array(d * n, dtype=dtype, device=device)
