def irfft(a: ArrayLike, n: int | None = None,
          axis: int = -1, norm: str | None = None) -> Array:
  r"""Compute a one-dimensional inverse discrete Fourier transform for real input.

  JAX implementation of :func:`numpy.fft.irfft`.

  Args:
    a: real-valued input array.
    n: int. Specifies the dimension of the result along ``axis``. If not specified,
      ``n = 2*(m-1)``, where ``m`` is the dimension of ``a`` along ``axis``.
    axis: int, default=-1. Specifies the axis along which the transform is computed.
      If not specified, the transform is computed along axis -1.
    norm: string. The normalization mode. "backward", "ortho" and "forward" are
      supported.

  Returns:
    An array containing the one-dimensional inverse discrete Fourier transform
    of ``a``, with a dimension of ``n`` along ``axis``.

  See also:
    - :func:`jax.numpy.fft.ifft`: Computes a one-dimensional inverse discrete
      Fourier transform.
    - :func:`jax.numpy.fft.irfft`: Computes a one-dimensional inverse discrete
      Fourier transform for real input.
    - :func:`jax.numpy.fft.rfftn`: Computes a multidimensional discrete Fourier
      transform for real input.
    - :func:`jax.numpy.fft.irfftn`: Computes a multidimensional inverse discrete
      Fourier transform for real input.

  Examples:
    ``jnp.fft.rfft`` computes the transform along ``axis -1`` by default.

    >>> x = jnp.array([[1, 3, 5],
    ...                [2, 4, 6]])
    >>> jnp.fft.irfft(x)
    Array([[ 3., -1.,  0., -1.],
           [ 4., -1.,  0., -1.]], dtype=float32)

    When ``n=3``, dimension of the transform along axis -1 will be ``3`` and
    dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.irfft(x, n=3)
    Array([[ 2.33, -0.67, -0.67],
           [ 3.33, -0.67, -0.67]], dtype=float32)

    When ``n=4`` and ``axis=0``, dimension of the transform along ``axis 0`` will
    be ``4`` and dimension along other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.fft.irfft(x, n=4, axis=0)
    Array([[ 1.25,  2.75,  4.25],
           [ 0.25,  0.75,  1.25],
           [-0.75, -1.25, -1.75],
           [ 0.25,  0.75,  1.25]], dtype=float32)
  """
  return _fft_core_1d('irfft', xla_client.FftType.IRFFT, a, n=n, axis=axis,
                      norm=norm)
