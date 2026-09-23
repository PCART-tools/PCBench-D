def rfftfreq(n: int, d: ArrayLike = 1.0, *, dtype: DTypeLike | None = None,
             device: xla_client.Device | Sharding | None = None) -> Array:
  """Return sample frequencies for the discrete Fourier transform.

  JAX implementation of :func:`numpy.fft.fftfreq`. Returns frequencies appropriate
  for use with the outputs of :func:`~jax.numpy.fft.rfft` and
  :func:`~jax.numpy.fft.irfft`.

  Args:
    n: length of the FFT window
    d: optional scalar sample spacing (default: 1.0)
    dtype: optional dtype of returned frequencies. If not specified, JAX's default
      floating point dtype will be used.
    device: optional :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of sample frequencies, length ``n // 2 + 1``.

  See also:
    - :func:`jax.numpy.fft.rfftfreq`: frequencies for use with
      :func:`~jax.numpy.fft.fft` and :func:`~jax.numpy.fft.ifft`.
  """
  dtype = dtype or dtypes.canonicalize_dtype(jnp.float_)
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

  result = k / jnp.array(d * n, dtype=dtype)

  if device is not None:
    return result.to_device(device)
  return result
