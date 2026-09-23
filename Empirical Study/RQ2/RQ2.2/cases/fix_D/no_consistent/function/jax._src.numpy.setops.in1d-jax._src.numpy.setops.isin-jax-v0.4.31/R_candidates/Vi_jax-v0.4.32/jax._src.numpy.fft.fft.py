def fft(a: ArrayLike, n: int | None = None,
        axis: int = -1, norm: str | None = None) -> Array:
  r"""Compute a one-dimensional discrete Fourier transform along a given axis.

  JAX implementation of :func:`numpy.fft.fft`.

  Args:
    a: input array
    n: int. Specifies the dimension of the result along ``axis``. If not specified,
      it will default to the dimension of ``a`` along ``axis``.
    axis: int, default=-1. Specifies the axis along which the transform is computed.
      If not specified, the transform is computed along axis -1.
    norm: string. The normalization mode. "backward", "ortho" and "forward" are
      supported.

  Returns:
    An array containing the one-dimensional discrete Fourier transform of ``a``.

  See also:
    - :func:`jax.numpy.fft.ifft`: Computes a one-dimensional inverse discrete
      Fourier transform.
    - :func:`jax.numpy.fft.fftn`: Computes a multidimensional discrete Fourier
      transform.
    - :func:`jax.numpy.fft.ifftn`: Computes a multidimensional inverse discrete
      Fourier transform.

  Examples:
    ``jnp.fft.fft`` computes the transform along ``axis -1`` by default.

    >>> x = jnp.array([[1, 2, 4, 7],
    ...                [5, 3, 1, 9]])
    >>> jnp.fft.fft(x)
    Array([[14.+0.j, -3.+5.j, -4.+0.j, -3.-5.j],
           [18.+0.j,  4.+6.j, -6.+0.j,  4.-6.j]], dtype=complex64)

    When ``n=3``, dimension of the transform along axis -1 will be ``3`` and
    dimension along other axes will be the same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.fft(x, n=3))
    [[ 7.+0.j   -2.+1.73j -2.-1.73j]
     [ 9.+0.j    3.-1.73j  3.+1.73j]]

    When ``n=3`` and ``axis=0``, dimension of the transform along ``axis 0`` will
    be ``3`` and dimension along other axes will be same as that of input.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.fft.fft(x, n=3, axis=0))
    [[ 6. +0.j    5. +0.j    5. +0.j   16. +0.j  ]
     [-1.5-4.33j  0.5-2.6j   3.5-0.87j  2.5-7.79j]
     [-1.5+4.33j  0.5+2.6j   3.5+0.87j  2.5+7.79j]]

    ``jnp.fft.ifft`` can be used to reconstruct ``x`` from the result of
    ``jnp.fft.fft``.

    >>> x_fft = jnp.fft.fft(x)
    >>> jnp.allclose(x, jnp.fft.ifft(x_fft))
    Array(True, dtype=bool)
  """
  return _fft_core_1d('fft', xla_client.FftType.FFT, a, n=n, axis=axis,
                      norm=norm)
